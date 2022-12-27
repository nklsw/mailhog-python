from mailhog import Mailhog

from .utils import run_around_tests, send_emails, server_send_email  # noqa: F401


def test_search_emails():
    """
    Test if email is found and if it is correct
    """
    # send email
    send_emails(10)

    mailhog = Mailhog()

    # check if all emails would be found
    messages = mailhog.search("Test Text")
    assert messages.total == 10

    # check if email with specific text could be found
    messages = mailhog.search("Test Text 0")
    assert messages.total == 1

    # check if email is correct
    assert messages.items[0].from_.mailbox == "from0"
    assert messages.items[0].from_.domain == "test.com"
    assert messages.items[0].to[0].mailbox == "to0"
    assert messages.items[0].to[0].domain == "test.com"
    assert messages.items[0].content.body == "Test Text 0"

    # check if email with specific from could be found
    messages = mailhog.search("from1@test.com", "from")
    assert messages.total == 1

    # check if email with specific to could be found
    messages = mailhog.search("to2@test.com", "to")
    assert messages.total == 1


def test_search_nonexisting_email():
    """
    Test if nonexisting email is not found
    """
    # send email
    send_emails(3)

    mailhog = Mailhog()

    # check if email is not found
    messages = mailhog.search("Test Text 5")
    assert len(messages.items) == 0

    # check if email with specific from is not found
    messages = mailhog.search("non@test.com", "from")
    assert len(messages.items) == 0

    # check if email with specific to is not found
    messages = mailhog.search("non@test.com", "to")
    assert len(messages.items) == 0


def test_search_with_limit_and_start():
    """
    Test if email is found and if it is correct
    """
    # send email
    send_emails(10)

    mailhog = Mailhog()

    # check if all emails would be found
    messages = mailhog.search("Test Text", limit=5, start=2)
    assert messages.total == 10
    assert len(messages.items) == 5

    # check if email with specific text could be found
    messages = mailhog.search("Test Text", limit=5, start=2)
    assert len(messages.items) == 5

    # check if email with specific from could be found
    messages = mailhog.search("from2@test.com", kind="from", limit=5)
    assert len(messages.items) == 1

    # check if email with specific to could be found
    messages = mailhog.search("to8@test.com", "to", limit=5)
    assert messages.total == 1
