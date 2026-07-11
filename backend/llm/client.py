from ollama import chat

from backend.config import LLMConfig


class OllamaClient:
    """
    Low-level client responsible for communicating with Ollama.
    """

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = chat(
            model=LLMConfig.MODEL,
            messages=messages,
            options={
                "temperature": LLMConfig.TEMPERATURE,
            },
        )

        return response["message"]["content"]