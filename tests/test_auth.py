"""Authentication tests"""
import pytest

@pytest.mark.asyncio
class TestAuth:
    async def test_register(self, client):
        response = await client.post("/api/v1/auth/register", json={"username": "newuser", "email": "new@example.com", "password": "password123"})
        assert response.status_code == 201
        assert response.json()["username"] == "newuser"
    
    async def test_login(self, client, test_user):
        response = await client.post("/api/v1/auth/login", data={"username": "testuser", "password": "testpassword"})
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    async def test_get_me(self, client, auth_headers):
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
