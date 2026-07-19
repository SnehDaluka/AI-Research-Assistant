from backend.config import ConversationConfig
from backend.prompts.builder import build_prompt
from backend.api.schemas.chat import ChatResponse, SourceResponse

class ResearchAssistantService:

    def __init__(
        self,
        retrieval_pipeline,
        context_builder,
        answer_generator,
        conversation_formatter,
        session_service,
    ):
        self.retrieval_pipeline = (
            retrieval_pipeline
        )

        self.context_builder = (
            context_builder
        )

        self.answer_generator = (
            answer_generator
        )

        self.conversation_formatter = (
            conversation_formatter
        )

        self.session_service = (
            session_service
        )

    def create_session(self) -> str:

        return self.session_service.create_session()

    def delete_session(
        self,
        session_id: str,
    ):
        self.session_service.delete_session(
            session_id
        )

    def ask(self, session_id: str, question: str):
        
        memory = self.session_service.get_memory(session_id)
        
        summary = memory.get_summary()
        rewrite_history = memory.get_recent_turns(limit=ConversationConfig.GENERATION_HISTORY_TURNS)
        
        results, trace = self.retrieval_pipeline.search(
            query=question,
            recent_turns=rewrite_history,
            summary=summary
        )
        
        context = self.context_builder.build(results)
        
        generation_history = memory.get_recent_turns(limit=ConversationConfig.GENERATION_HISTORY_TURNS)
        formatted_conversation = self.conversation_formatter.format(generation_history)
        
        prompt = build_prompt(
            query=question,
            context=context,
            conversation=formatted_conversation,
            conversation_summary=summary
        )
        
        answer = self.answer_generator.generate(prompt)
        
        memory.add_turn(user=question, assistant=answer)
        
        sources = []
        seen = set()
        for result in results:
            filename = result.document.source.filename
            
            # Only include the source if the LLM actually cited it in the generated answer
            if filename in answer:
                key = (filename, result.document.page)
                if key not in seen:
                    seen.add(key)
                    sources.append(
                        SourceResponse(
                            source=filename,
                            page=result.document.page,
                            score=result.score
                        )
                    )
            
        return ChatResponse(
            answer=answer,
            sources=sources
        )