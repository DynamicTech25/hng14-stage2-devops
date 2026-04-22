from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")  # FIXED endpoint
    assert response.status_code == 200
    assert response.json()["message"] == "API is running"


@patch("api.main.get_redis")
def test_create_job(mock_get_redis):
    mock_r = mock_get_redis.return_value

    mock_r.lpush.return_value = 1
    mock_r.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()

    assert "job_id" in data
    assert isinstance(data["job_id"], str)


@patch("api.main.get_redis")
def test_get_job_status(mock_get_redis):
    mock_r = mock_get_redis.return_value

    mock_r.hget.return_value = "queued"

    response = client.get("/jobs/test-id")

    assert response.status_code == 200
    data = response.json()

    assert data["job_id"] == "test-id"
    assert data["status"] == "queued"
