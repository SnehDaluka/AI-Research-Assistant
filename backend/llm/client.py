from ollama import chat

from backend.config import LLMConfig


def generate_response(messages):
    """
    Send chat messages to the LLM and return the response.
    """

    response = chat(
        model=LLMConfig.MODEL,
        messages=messages
    )

    return response["message"]["content"]