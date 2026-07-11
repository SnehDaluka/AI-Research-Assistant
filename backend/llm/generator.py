class AnswerGenerator:
    """
    Generates the final answer using the LLM.
    """

    def __init__(self, llm_service):
        self.llm_service = llm_service

    def generate(self, prompt: str) -> str:
        """
        Generate an answer from the final RAG prompt.
        """

        return self.llm_service.generate(prompt)