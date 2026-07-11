class ConversationFormatter:
    """
    Formats conversation messages for LLM prompts.
    """

    def format(
        self,
        messages,
    ) -> str:

        if not messages:
            return "No previous conversation."

        formatted_messages = []

        for message in messages:

            role = message.role.capitalize()

            formatted_messages.append(
                f"{role}: {message.content}"
            )

        return "\n\n".join(
            formatted_messages
        )