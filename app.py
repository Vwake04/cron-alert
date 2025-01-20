import os
import time
from functools import partial

import schedule

from db import init_db
from notify import check_upgrades
from logger import setup_logging

# Set up logging
logger = setup_logging()

# Initialize database
logger.info("Initializing database...")
engine = init_db()


def get_schedule_times():
    """Get schedule times from environment variable."""
    default_times = ["09:00", "21:00"]
    schedule_str = os.getenv("SCHEDULE_TIMES")

    if not schedule_str:
        logger.info(f"No schedule times configured, using defaults: {default_times}")
        return default_times

    # Split the string and clean up each time
    times = [t.strip() for t in schedule_str.split(",")]

    # Validate times (HH:MM format)
    valid_times = []
    for t in times:
        try:
            hour, minute = map(int, t.split(":"))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                valid_times.append(f"{hour:02d}:{minute:02d}")
            else:
                logger.warning(f"Invalid time format {t}, skipping...")
        except ValueError:
            logger.warning(f"Invalid time format {t}, skipping...")

    if not valid_times:
        logger.warning(f"No valid times found, using defaults: {default_times}")
        return default_times

    logger.info(f"Using configured schedule times: {valid_times}")
    return valid_times


def main():
    try:
        # Get schedule times from environment
        schedule_times = get_schedule_times()

        # Schedule the job for each time
        for time_str in schedule_times:
            schedule.every().day.at(time_str).do(partial(check_upgrades, engine))
            logger.info(f"Scheduled upgrade check for {time_str}")

        # Run every 30 seconds
        # schedule.every(30).seconds.do(partial(check_upgrades, engine))
        # logger.info("Scheduled upgrade check every 30 seconds")

        logger.info("Notification service started...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Wait for one minute before checking again
            logger.info("Checking for upgrades...")
    except Exception as e:
        logger.exception(f"Fatal error in main loop: {str(e)}")
        raise


if __name__ == "__main__":
    main()
