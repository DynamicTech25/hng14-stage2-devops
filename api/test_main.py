from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "message" in response.json()


@patch("main.r")
def test_create_job(mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data


@patch("main.r")
def test_get_job_not_found(mock_redis):
    mock_redis.hget.return_value = None

    response = client.get("/jobs/invalid-id")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["not found", None]