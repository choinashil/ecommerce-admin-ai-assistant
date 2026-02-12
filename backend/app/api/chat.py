from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import ChatRequest
from app.services.chat_service import stream_chat

router = APIRouter()


@router.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    return StreamingResponse(
        stream_chat(db, request.message, request.conversation_id),
        media_type="text/event-stream",
    )
