import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch
from controllers.v1.job_searching_controller import router as job_search_router

app = FastAPI()
app.include_router(job_search_router)

@pytest.fixture(scope="class")
def client():
    return TestClient(app)


mock_job = {
    "_id": "68e68a4025035785b7c93f3f",
    "user_id": "123",
    "title": "Backend Developer",
    "description": "Build APIs and service",
    "company": "Zaptide",
    "location": "Hyderabad",
    "salary": 1200000.0,
    "posted_date": "2025-10-08T12:00:00",
    "is_active": True
}

@pytest.mark.usefixtures("client")
class TestJobPostingController:

    def test_get_job_by_id_success(self,client):
        job_id = "68e68a4025035785b7c93f3f"

        with patch("controllers.v1.job_searching_controller.db") as mock_db:
            mock_db.jobs.find_one = AsyncMock(return_value=mock_job)

            response = client.get(f"/v1/jobs/{job_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["_id"] == job_id
            assert data["title"] == "Backend Developer"
            assert data["user_id"] == "123"


    def test_get_job_by_id_not_found(self,client):
        job_id = "68e68a4025035785b7c93f3a"

        with patch("controllers.v1.job_searching_controller.db") as mock_db:
            mock_db.jobs.find_one = AsyncMock(return_value=None)

            response = client.get(f"/v1/jobs/{job_id}")
            assert response.status_code == 404