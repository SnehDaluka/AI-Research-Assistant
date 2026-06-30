from ollama import chat

from backend.config import LLM_MODEL


def generate_response(messages):
    """
    Send chat messages to the LLM and return the response.
    """

    response = chat(
        model=LLM_MODEL,
        messages=messages
    )

    return response["message"]["content"]