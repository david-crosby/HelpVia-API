"""Tickets API"""
import logging
import math
from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.ticket import Ticket, TicketStatus
from app.models.user import User
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse, TicketListResponse, TicketAction

logger = logging.getLogger("helpvia")
router = APIRouter()

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_data: TicketCreate, current_user: Annotated[User, Depends(get_current_active_user)], db: AsyncSession = Depends(get_db)):
    ticket = Ticket(summary=ticket_data.summary, description=ticket_data.description, status=ticket_data.status, priority=ticket_data.priority, created_by_id=current_user.id)
    return await TicketRepository(db).create(ticket)

@router.get("/", response_model=TicketListResponse)
async def get_all_tickets(current_user: Annotated[User, Depends(get_current_active_user)], db: AsyncSession = Depends(get_db), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), status: Optional[TicketStatus] = None):
    repo = TicketRepository(db)
    skip = (page - 1) * page_size
    tickets = await repo.get_all(skip=skip, limit=page_size, status=status)
    total = await repo.count_all(status=status)
    return TicketListResponse(total=total, items=tickets, page=page, page_size=page_size, total_pages=math.ceil(total / page_size))

@router.get("/open", response_model=TicketListResponse)
async def get_open_tickets(current_user: Annotated[User, Depends(get_current_active_user)], db: AsyncSession = Depends(get_db), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    repo = TicketRepository(db)
    skip = (page - 1) * page_size
    tickets = await repo.get_open_tickets(skip=skip, limit=page_size)
    total = await repo.count_all(TicketStatus.OPEN) + await repo.count_all(TicketStatus.IN_PROGRESS)
    return TicketListResponse(total=total, items=tickets, page=page, page_size=page_size, total_pages=math.ceil(total / page_size))

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int, current_user: Annotated[User, Depends(get_current_active_user)], db: AsyncSession = Depends(get_db)):
    ticket = await TicketRepository(db).get_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return ticket

@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: int, ticket_data: TicketUpdate, current_user: Annotated[User, Depends(get_current_active_user)], db: AsyncSession = Depends(get_db)):
    repo = TicketRepository(db)
    ticket = await repo.get_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    update_data = ticket_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    if "status" in update_data:
        ticket.add_action(f"Status changed to {update_data['status'].value}", current_user.username)
        if update_data["status"] == TicketStatus.CLOSED:
            ticket.closed_at = datetime.utcnow()
    return await repo.update(ticket)

@router.post("/{ticket_id}/actions", response_model=TicketResponse)
async def add_ticket_action(ticket_id: int, action_data: TicketAction, current_user: Annotated[User, Depends(get_current_active_user)], db: AsyncSession = Depends(get_db)):
    repo = TicketRepository(db)
    ticket = await repo.get_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    ticket.add_action(action_data.action, current_user.username)
    return await repo.update(ticket)

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id: int, current_user: Annotated[User, Depends(get_current_active_user)], db: AsyncSession = Depends(get_db)):
    if not await TicketRepository(db).delete(ticket_id):
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
