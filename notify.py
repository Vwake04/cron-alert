import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

from loguru import logger
from sqlmodel import select

from db import Session
from models import Upgrade


def send_upgrade_notification(to_email: str, server: str):
    # Get SMTP settings from environment variables with Gmail defaults
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    # For Gmail, you need to use an App Password if 2FA is enabled
    # Generate one at: https://myaccount.google.com/apppasswords
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_username or not smtp_password:
        logger.error(
            "SMTP credentials not configured. Please set SMTP_USERNAME and SMTP_PASSWORD"
        )
        return

    msg = MIMEText(f"An upgrade is due for server: {server}")
    msg["Subject"] = "Server Upgrade Notification"
    msg["From"] = smtp_username
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        logger.info(f"Notification sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")


def check_upgrades(engine):
    try:
        with Session(engine) as session:
            # Get all upgrades where next_upgrade is due
            statement = select(Upgrade).where(Upgrade.next_upgrade <= datetime.now())
            results = session.exec(statement).all()

            if not results:
                logger.info("No upgrades due at this time")
                return

            logger.info(f"Found {len(results)} upgrades due for notification")
            for upgrade in results:
                logger.debug(
                    f"Processing upgrade notification for server: {upgrade.server} and email: {upgrade.email}"
                )
                send_upgrade_notification(upgrade.email, upgrade.server)
    except Exception as e:
        logger.exception(f"Error checking upgrades: {str(e)}")
