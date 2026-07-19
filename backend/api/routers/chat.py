from fastapi import APIRouter
from fastapi import Depends

from backend.api.dependencies import (
    get_application,
    get_current_user,
)

from backend.api.schemas.chat import (
    ChatRequest,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("")
def chat(
    request: ChatRequest,
    application=Depends(get_application),
    current_user=Depends(get_current_user),
):

    response = (
        application.assistant_service.ask(
            session_id=request.session_id,
            question=request.question,
        )
    )

    return response