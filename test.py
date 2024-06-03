import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.responses import StreamingResponse


@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(base_url="http://127.0.0.1:8000/query") as ac:
        query = {"message": "What is the weather today?"}
        response = await ac.post("/", json=query)

        assert response.status_code == 200
        # Read the streaming response
        async for line in response.aiter_lines():
            assert "chunk" in line  # Replace with actual expected response content


if __name__ == "__main__":
    pytest.main()