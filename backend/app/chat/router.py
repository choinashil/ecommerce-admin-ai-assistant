from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.shared.database import get_db
from app.shared.display_id import parse_pk
from app.chat.model import Conversation
from app.chat.schema import ChatRequest, ConversationSummary, MessageDetail
from app.chat.service import stream_chat
from app.chat.history import get_conversations, get_messages

router = APIRouter()


@router.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    return StreamingResponse(
        stream_chat(db, request.message, conversation_display_id=request.conversation_id),
        media_type="text/event-stream",
    )


@router.get("/api/conversations", response_model=list[ConversationSummary])
def list_conversations(db: Session = Depends(get_db)):
    return get_conversations(db)


@router.get(
    "/api/conversations/{display_id}/messages",
    response_model=list[MessageDetail],
)
def list_messages(display_id: str, db: Session = Depends(get_db)):
    pk = parse_pk(display_id, "conversations")
    conversation = db.get(Conversation, pk)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return get_messages(db, pk)
