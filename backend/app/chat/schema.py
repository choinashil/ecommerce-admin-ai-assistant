from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ToolCallDetail(BaseModel):
    name: str
    arguments: dict
    result: dict


class MessageMetadata(BaseModel):
    model: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    response_time_ms: int | None = None
    system_prompt: str | None = None
    error: str | None = None
    aborted: bool | None = None
    tool_calls: list[ToolCallDetail] | None = None


class MessageDetail(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime
    metadata: MessageMetadata | None = None


class ConversationSummary(BaseModel):
    id: str
    first_message: str
    message_count: int
    total_tokens: int
    created_at: datetime
    updated_at: datetime
    seller_id: str | None = None
    seller_nickname: str | None = None
