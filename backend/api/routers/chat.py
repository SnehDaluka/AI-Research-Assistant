from fastapi import APIRouter
from fastapi import Depends, Request
import asyncio
from fastapi.concurrency import run_in_threadpool

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
async def chat(
    request: Request,
    chat_request: ChatRequest,
    application=Depends(get_application),
    current_user=Depends(get_current_user),
):
    cancel_flag = {"is_cancelled": False}

    async def check_disconnect():
        while True:
            if await request.is_disconnected():
                cancel_flag["is_cancelled"] = True
                break
            await asyncio.sleep(0.5)

    task = asyncio.create_task(check_disconnect())

    try:
        response = await run_in_threadpool(
            application.assistant_service.ask,
            chat_request.session_id,
            chat_request.question,
            cancel_flag
        )
        return response
    finally:
        task.cancel()