import base64
import quopri
from email.message import EmailMessage

from mailhog import Mailhog

from .utils import run_around_tests, send_emails, server_send_email  # noqa: F401


def test_get_email():
    """
    Test if email is received and if it is correct
    """
    # send email
    send_emails(1)

    # check if email is received
    mailhog = Mailhog()

    messages = mailhog.messages()
    assert messages.total == 1

    print(type(messages.items[0]))

    # check if email is correct
    assert messages.items[0].from_.mailbox == "from0"
    assert messages.items[0].from_.domain == "test.com"
    assert messages.items[0].to[0].mailbox == "to0"
    assert messages.items[0].to[0].domain == "test.com"
    assert messages.items[0].content.body == "Test Text 0"


def test_get_multiple_emails():
    """
    Test if multiple emails are received and if they are correct
    """
    # send emails
    send_emails(3)

    # check if emails are received
    mailhog = Mailhog()

    messages = mailhog.messages()
    assert messages.total == 3


def test_get_email_with_attachment():
    """
    Test if email with attachment is received and if it is correct
    """
    # send  Emailmessage
    msg = EmailMessage()
    msg["Subject"] = "Test"
    msg["From"] = "from@test.com"
    msg["To"] = "to@test.com"
    msg.set_content("Test Text", subtype="plain")

    with open("tests/test.txt", "rb") as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(
        file_data, maintype="application", subtype="octet-stream", filename=file_name
    )
    server_send_email(msg)

    # check if email is received
    mailhog = Mailhog()

    messages = mailhog.messages()
    assert messages.total == 1

    # check if email is correct
    assert messages.items[0].from_.mailbox == "from"
    assert messages.items[0].from_.domain == "test.com"
    assert messages.items[0].to[0].mailbox == "to"
    assert messages.items[0].to[0].domain == "test.com"

    # try to decode text and retry if failed
    try:
        text = quopri.decodestring(messages.items[0].mime.parts[0].body).decode("utf-8")
    except UnicodeDecodeError:
        text = quopri.decodestring(messages.items[0].mime.parts[0].body).decode("utf-8")

    assert "Test Text" in text

    # check if attachment is correct
    assert "test.txt" in messages.items[0].mime.parts[1].headers["Content-Disposition"]
    assert (
        messages.items[0].mime.parts[1].headers["Content-Type"]
        == "['application/octet-stream']"
    )
    assert (
        base64.b64decode(messages.items[0].mime.parts[1].body).decode("utf-8")
        == "Test Attachment"
    )


def test_with_limit_and_start():
    """
    Test if emails are received with limit and start
    """
    # send emails
    send_emails(3)

    # check if emails are received
    mailhog = Mailhog()

    messages = mailhog.messages(start=1, limit=1)
    assert messages.total == 3
    assert len(messages.items) == 1


def test_get_empty_result():
    """
    Test if nonexisting email is not received
    """
    # send email
    send_emails(1)

    # check if email is not received
    mailhog = Mailhog()

    messages = mailhog.messages(start=2, limit=0)
    assert len(messages.items) == 0


def test_message_functions():
    """
    Test if functions of Message class work
    """
    # send email
    send_emails(1)

    # check if email is received
    mailhog = Mailhog()

    messages = mailhog.messages()
    assert messages.total == 1

    # check if functions work
    assert messages.items[0].get_sender() == "from0@test.com"
    assert messages.items[0].get_recipients() == ["to0@test.com"]
    assert messages.items[0].get_subject() == "Test 0"


def test_delete_message():
    """
    Test if individual messages can be deleted.
    """
    send_emails(1)

    mailhog = Mailhog()
    messages = mailhog.messages()
    mailhog.delete(messages.items[0])
    assert mailhog.messages().total == 0
