from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

class ChatMessageTurn(BaseModel):
    role: str = Field(..., description="'user' hoặc 'assistant' / 'model'")
    content: str = Field(..., max_length=2000, description="Nội dung tin nhắn trong lịch sử")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        role = v.lower().strip()
        if role in ['user', 'human']:
            return 'user'
        if role in ['assistant', 'ai', 'model']:
            return 'model'
        return 'user'

class ChatbotRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="Nội dung câu hỏi của người dùng")
    conversation_id: Optional[str] = Field(None, description="Mã định danh phiên hội thoại")
    history: Optional[List[ChatMessageTurn]] = Field(default_factory=list, description="Lịch sử đối thoại gần nhất (tối đa 10 lượt)")

    @field_validator('message')
    @classmethod
    def validate_message_not_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Câu hỏi không được để trống hoặc chỉ chứa khoảng trắng.")
        return stripped

    @field_validator('history')
    @classmethod
    def limit_history_turns(cls, v: Optional[List[ChatMessageTurn]]) -> List[ChatMessageTurn]:
        if not v:
            return []
        # Giới hạn tối đa 10 lượt tin nhắn gần nhất để bảo vệ token & tránh tấn công prompt injection
        return v[-10:]

class ChatbotResponse(BaseModel):
    success: bool = True
    conversation_id: str
    reply: str
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    provider: str
    error: Optional[str] = None
    timestamp: str
