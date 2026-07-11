from backend.config import ConversationConfig
from backend.conversation.message import Message


class ConversationMemory:
    """
    Stores recent conversation messages in memory.
    """

    def __init__(
        self,
        max_messages: int = ConversationConfig.MAX_STORED_MESSAGES,
    ):
        self.max_messages = max_messages
        self.messages = []

    def add_user_message(
        self,
        content: str,
    ):
        self._add_message(
            role="user",
            content=content,
        )

    def add_assistant_message(
        self,
        content: str,
    ):
        self._add_message(
            role="assistant",
            content=content,
        )

    def _add_message(
        self,
        role: str,
        content: str,
    ):
        self.messages.append(
            Message(
                role=role,
                content=content,
            )
        )

        self._trim()

    def _trim(self):
        """
        Keep only the most recent messages.
        """

        if len(self.messages) > self.max_messages:
            self.messages = self.messages[
                -self.max_messages:
            ]

    def get_messages(
        self,
        limit: int | None = ConversationConfig.GENERATION_HISTORY_MESSAGES,
    ):
        """
        Return a copy of recent conversation messages.
        """

        if limit is None:
            return self.messages.copy()

        return self.messages[-limit:].copy()

    def clear(self):
        """
        Clear all conversation history.
        """

        self.messages.clear()