from db import init_db, Session
from models import Upgrade
from datetime import datetime, timedelta


def add_test_data():
    engine = init_db()

    with Session(engine) as session:
        test_upgrade1 = Upgrade(
            server="test-server-1",
            last_upgraded=datetime.now() - timedelta(days=30),
            next_upgrade=datetime.now() + timedelta(days=1),
            email="baraiyavivek04@gmail.com",
        )
        test_upgrade2 = Upgrade(
            server="test-server-2",
            last_upgraded=datetime.now() - timedelta(days=30),
            next_upgrade=datetime.now(),  # Due now
            email="baraiyawake04@gmail.com",
        )
        test_upgrade3 = Upgrade(
            server="test-server-3",
            last_upgraded=datetime.now() - timedelta(days=30),
            next_upgrade=datetime.now(),
            email="baraiyawake04@gmail.com",
        )

        session.add(test_upgrade1)
        session.add(test_upgrade2)
        session.add(test_upgrade3)
        session.commit()


if __name__ == "__main__":
    add_test_data()
