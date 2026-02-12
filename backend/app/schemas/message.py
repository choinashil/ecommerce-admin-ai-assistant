from datetime import datetime

from pydantic import BaseModel


class MessageMetadata(BaseModel):
    model: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    response_time_ms: int | None = None
    system_prompt: str | None = None
    error: str | None = None


class MessageDetail(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime
    metadata: MessageMetadata | None = None
