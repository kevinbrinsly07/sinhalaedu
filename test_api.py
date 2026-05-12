"""Test suite for Sinhala Exam Paper Generator."""

import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_list_subjects():
    """Test list subjects endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/papers/subjects")
        assert response.status_code == 200
        data = response.json()
        assert "subjects" in data
        assert len(data["subjects"]) > 0


@pytest.mark.asyncio
async def test_generate_paper_invalid_input():
    """Test paper generation with invalid input."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/papers/generate",
            json={
                "subject": "",
                "grade": 0,
            }
        )
        # Should fail validation
        assert response.status_code != 200


# Add more tests as needed
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
