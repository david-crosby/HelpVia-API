"""Ticket schemas"""
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field, ConfigDict
from app.models.ticket import TicketStatus, TicketPriority

class TicketBase(BaseModel):
    summary: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TicketStatus = TicketStatus.OPEN
    priority: TicketPriority = TicketPriority.MEDIUM

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    summary: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_to_id: Optional[int] = None

class TicketAction(BaseModel):
    action: str = Field(..., min_length=1)

class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None
    actions: Dict[str, dict] = Field(default_factory=dict)
    assigned_to_id: Optional[int] = None
    created_by_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class TicketListResponse(BaseModel):
    total: int
    items: list[TicketResponse]
    page: int
    page_size: int
    total_pages: int
