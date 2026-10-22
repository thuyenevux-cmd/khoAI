from typing import Dict, Any, Optional
from pydantic import BaseModel

class AIAnalysisRequest(BaseModel):
    period: Optional[str] = "30_DAYS"  # 30_DAYS, THIS_MONTH, LAST_MONTH, ALL

class AIAnalysisResponse(BaseModel):
    success: bool = True
    feature: str
    period: str
    markdown_report: str
    data_snapshot: Dict[str, Any]
    provider: str

class AIAssistantRequest(BaseModel):
    question: str

class AIAssistantResponse(BaseModel):
    success: bool = True
    question: str
    answer_markdown: str
    data_context: Optional[Dict[str, Any]] = None
    provider: str
    timestamp: str
