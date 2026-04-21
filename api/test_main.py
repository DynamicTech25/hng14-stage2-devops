from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert data["message"] == "API is running"


@patch("main.get_redis")
def test_create_job(mock_get_redis):
    # Fake Redis instance
    mock_r = mock_get_redis.return_value

    # Mock Redis methods used in create_job
    mock_r.lpush.return_value = 1
    mock_r.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200

    data = response.json()
    assert "job_id" in data
    assert isinstance(data["job_id"], str)


@patch("main.get_redis")
def test_get_job_not_found(mock_get_redis):
    # Fake Redis instance
    mock_r = mock_get_redis.return_value

    # Simulate missing job
    mock_r.hget.return_value = None

    response = client.get("/jobs/invalid-id")

    assert response.status_code == 200

    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"
