from dataclasses import dataclass


@dataclass(slots=True)
class Message:
    """
    Represents one message in the conversation.
    """

    role: str
    content: str