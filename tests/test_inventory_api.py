import pytest
from httpx import AsyncClient, ASGITransport
from inventory.app import app

@pytest.mark.asyncio
async def test_create_and_get_item():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/items", json={"name": "apple", "quantity": 5})
        assert r.status_code == 201

        r2 = await ac.get("/items/apple")
        assert r2.status_code == 200
        assert r2.json()["quantity"] == 5

        await ac.delete("/items/apple")
