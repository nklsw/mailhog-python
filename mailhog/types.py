from dataclasses import dataclass
from typing import Dict, List, Union

from dataclass_wizard import JSONWizard, json_field


@dataclass
class Path:
    """A path

    :param relays: The list of relays.
    :param mailbox: The mailbox.
    :param domain: The domain.
    :param params: The parameters.

    :raises ValueError: If the JSON is invalid.
    """

    relays: Union[List[str], None]
    mailbox: str
    domain: str
    params: str


@dataclass
class MIME:
    """A MIME type"""

    pass


@dataclass
class Content:
    """The content of a message

    :param headers: The headers of the message.
    :param body: The body of the message.
    :param size: The size of the message.
    :param mime: The MIME type of the message.

    :raises ValueError: If the JSON is invalid.
    """

    headers: Dict[str, str]
    body: str
    size: int
    mime: Union[MIME, None]


@dataclass
class MIMEContent:
    """A MIME part of a message

    :param headers: The headers of the part.
    :param body: The body of the part.
    :param size: The size of the part.
    :param mime: The MIME type of the part.

    :raises ValueError: If the JSON is invalid.
    """

    headers: Dict[str, str]
    body: str
    size: int
    mime: Union[MIME, None]


@dataclass
class MIMEBody:
    """The MIME body of a message

    :param parts: The list of MIMEContent parts.

    :raises ValueError: If the JSON is invalid.
    """

    parts: List[MIMEContent]


@dataclass
class Message:
    """A message from Mailhog

    :param id: The ID of the message.
    :param to: The list of recipients.
    :param created: The date the message was created.
    :param content: The content of the message.
    :param raw: The raw message.
    :param mime: The MIME body of the message.
    :param from_: The sender of the message.

    :raises ValueError: If the JSON is invalid.
    """

    id: str
    to: List[Path]
    created: str
    content: Content
    raw: Union[str, None]
    mime: Union[MIMEBody, None]
    from_: Path = json_field("From", all=True)

    def get_sender(self) -> str:
        """Get the sender of the message.

        :return: The sender of the message.
        """
        return f"{self.from_.mailbox}@{self.from_.domain}"

    def get_recipients(self) -> List[str]:
        """Get the recipients of the message.

        :return: The list of recipients of the message.
        """
        return [f"{path.mailbox}@{path.domain}" for path in self.to]

    def get_subject(self) -> str:
        """Get the subject of the message.

        :return: The subject.

        """

        if "Subject" in self.content.headers:
            return self.content.headers["Subject"][2:-2]
        return None


@dataclass
class Messages(JSONWizard):
    """_summary_

    Args:
        JSONWizard (_type_): _description_
    """

    total: int
    start: int
    count: int
    items: List[Message]
