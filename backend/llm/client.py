from ollama import chat

from backend.prompts.templates import SYSTEM_PROMPT
from backend.config import MODEL_NAME


def generate_response(user_prompt):
    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response["message"]["content"]