import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, ANY
from app.main import app
from app.config import settings

client = TestClient(app)


# Test the root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "server is running"}


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_process_data(mocked_httpx_post):
    task_id = 12345

    # Mock the response from the Node.js server
    mocked_httpx_post.return_value.status_code = 200
    mocked_httpx_post.return_value.json.return_value = {"status": "Success"}

    # Simulate sending the POST request to /ml/data/{task_id}
    response = client.post(f"/api/ml/data/{task_id}")

    # Assert that the request was successful
    assert response.status_code == 200

    # Check if the ML service processed and responded correctly
    assert response.json() == {
        "status": "Success",
        "message": f"Data for task {task_id} received. Processing in the background.",
    }

    # Verify that the mock was called with the correct parameters
    mocked_httpx_post.assert_called_once()

    # Get the expected URL
    expected_url = f"{settings.NODE_WEBHOOK_URL}/api/ml/result"

    # Assert that the request to the Node.js server was made to the expected URL
    mocked_httpx_post.assert_called_with(expected_url, json=ANY)


# Test invalid data handling
def test_process_data_invalid():
    # Attempt to send an invalid POST request with missing task_id in URL
    response = client.post("/ml/data/")

    # Assert that the validation error is returned
    assert response.status_code == 404  # Since task_id is a required path parameter

    # Optional: check for specific error details
    assert "detail" in response.json()
