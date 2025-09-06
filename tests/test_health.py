"""Tests for health endpoint."""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app


def test_health_endpoint():
    """Test health endpoint returns 200 with correct response."""
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_endpoint_async():
    """Test health endpoint with async client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
