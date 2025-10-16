"""Ticket tests"""
import pytest
from app.models.ticket import Ticket

@pytest.mark.asyncio
class TestTickets:
    async def test_create_ticket(self, client, auth_headers):
        response = await client.post("/api/v1/tickets/", json={"summary": "Test", "description": "Test ticket"}, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["summary"] == "Test"
    
    async def test_get_tickets(self, client, auth_headers):
        response = await client.get("/api/v1/tickets/", headers=auth_headers)
        assert response.status_code == 200
        assert "items" in response.json()
    
    async def test_get_ticket(self, client, auth_headers, db_session, test_user):
        ticket = Ticket(summary="Test", created_by_id=test_user.id)
        db_session.add(ticket)
        await db_session.commit()
        await db_session.refresh(ticket)
        response = await client.get(f"/api/v1/tickets/{ticket.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == ticket.id
