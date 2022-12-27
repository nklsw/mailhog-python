import smtplib
from email.mime.text import MIMEText

import pytest

from mailhog import Mailhog


@pytest.fixture(autouse=True)
def run_around_tests():
    """
    Delete all emails before and after each test
    """
    mailhog = Mailhog()
    mailhog.delete_all()
    yield
    mailhog.delete_all()


def server_send_email(msg) -> None:
    server = smtplib.SMTP("localhost", 1025)
    server.send_message(msg)


def send_emails(number) -> None:
    """
    Send emails using smtplib
    """
    for i in range(number):
        msg = MIMEText(f"Test Text {i}")
        msg["Subject"] = f"Test {i}"
        msg["From"] = f"from{i}@test.com"
        msg["To"] = f"to{i}@test.com"

        server_send_email(msg)
