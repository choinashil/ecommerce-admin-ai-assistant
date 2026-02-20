from datetime import datetime

from pydantic import BaseModel


class SellerResponse(BaseModel):
    token: str
    nickname: str


class SellerDetail(BaseModel):
    id: str
    nickname: str
    created_at: datetime
    last_active_at: datetime | None
    total_conversations: int
    total_messages: int
    total_tokens: int
