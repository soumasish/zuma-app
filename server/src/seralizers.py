
from pydantic import BaseModel
from typing import Optional


class Lead(BaseModel):
    name: str
    email: str


class Preferences(BaseModel):
    bedrooms: int
    move_in: str


class HumanMessageRequest(BaseModel):
    lead: Lead
    message: str
    preferences: Preferences
    community_id: str


class AgentResponse(BaseModel):
    reply: str
    action: str
    proposed_time: Optional[str] = None