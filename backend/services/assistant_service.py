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
        
        import re
        
        answer = self.answer_generator.generate(prompt)
        
        sources = []
        seen = set()
        for result in results:
            filename = result.document.source.filename
            
            # Check if LLM cited it. Loosen heuristic so sources aren't hidden if LLM omits extension
            # or uses a generic bracket citation.
            if filename in answer or filename.replace('.pdf', '') in answer or "[" in answer:
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

        # Clean citations from the text so they don't double up with the UI chips
        cleaned_answer = re.sub(r'\[[^\]]*(?:Page|page|PDF|pdf)\s*\d*[^\]]*\]', '', answer)
        cleaned_answer = re.sub(r'\[\d+\]', '', cleaned_answer)
        for result in results:
            filename = result.document.source.filename
            stem = filename.replace('.pdf', '')
            cleaned_answer = cleaned_answer.replace(f"[{filename}]", "").replace(f"[{stem}]", "")
            
        memory.add_turn(user=question, assistant=cleaned_answer)
        
        return ChatResponse(
            answer=cleaned_answer,
            sources=sources
        )