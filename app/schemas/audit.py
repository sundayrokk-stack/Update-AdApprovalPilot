from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

class AuditRequest(BaseModel):
    target_link: str = Field(..., description="The Telegram channel, bot, or profile link")
    issue_type: str = Field(..., description="The specific category of ad problem reported")

class AuditIssue(BaseModel):
    description: str
    severity: str  # Low, Medium, High
    recommendation: str

class AuditResponse(BaseModel):
    score: int = Field(ge=0, le=100)
    risk_level: str
    approval_probability: str
    issues: List[AuditIssue]
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
