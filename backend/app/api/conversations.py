from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.display_id import parse_pk
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationSummary
from app.schemas.message import MessageDetail
from app.services.conversation_service import get_conversations, get_messages

router = APIRouter()


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
