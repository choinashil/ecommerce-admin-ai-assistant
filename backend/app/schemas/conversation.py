from datetime import datetime

from pydantic import BaseModel


class ConversationSummary(BaseModel):
    id: str
    first_message: str
    message_count: int
    total_tokens: int
    created_at: datetime
