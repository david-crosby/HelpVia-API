"""Ticket repository"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket, TicketStatus

class TicketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, ticket: Ticket) -> Ticket:
        self.db.add(ticket)
        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket
    
    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        result = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100, status: Optional[TicketStatus] = None) -> List[Ticket]:
        query = select(Ticket)
        if status:
            query = query.where(Ticket.status == status)
        query = query.offset(skip).limit(limit).order_by(Ticket.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_open_tickets(self, skip: int = 0, limit: int = 100) -> List[Ticket]:
        query = select(Ticket).where(Ticket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS])).offset(skip).limit(limit).order_by(Ticket.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count_all(self, status: Optional[TicketStatus] = None) -> int:
        query = select(func.count(Ticket.id))
        if status:
            query = query.where(Ticket.status == status)
        result = await self.db.execute(query)
        return result.scalar() or 0
    
    async def update(self, ticket: Ticket) -> Ticket:
        ticket.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket
    
    async def delete(self, ticket_id: int) -> bool:
        ticket = await self.get_by_id(ticket_id)
        if ticket:
            await self.db.delete(ticket)
            await self.db.commit()
            return True
        return False
