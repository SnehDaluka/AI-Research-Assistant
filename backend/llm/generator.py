from backend.llm.client import generate_response
from backend.prompts.templates import SYSTEM_PROMPT


def generate_answer(user_prompt):
    """
    Generate an answer using the LLM.
    """

    if user_prompt is None:
        return "I couldn't find any relevant information."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    return generate_response(messages)