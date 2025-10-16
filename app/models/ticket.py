"""Ticket database model"""
from datetime import datetime
import json
import enum
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ON_HOLD = "on_hold"

class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    closed_at = Column(DateTime)
    actions_json = Column(Text, default="{}")
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_tickets")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="created_tickets")
    
    @property
    def actions(self) -> dict:
        try:
            return json.loads(self.actions_json) if self.actions_json else {}
        except:
            return {}
    
    @actions.setter
    def actions(self, value: dict):
        self.actions_json = json.dumps(value) if value else "{}"
    
    def add_action(self, action: str, user: str, timestamp=None):
        timestamp = timestamp or datetime.utcnow()
        current = self.actions
        current[timestamp.isoformat()] = {"action": action, "user": user, "timestamp": timestamp.isoformat()}
        self.actions = current
