import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch
from controllers.v1.job_posting_controller import router as job_router

app = FastAPI()
app.include_router(job_router)

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

    def test_create_job_posting_success(self,client):
        job_payload = {
            "user_id": "123",
            "title": "Backend Developer",
            "description": "Build APIs and service",
            "company": "Zaptide",
            "location": "Hyderabad",
            "salary": 1200000.0,
            "posted_date": "2025-10-08T12:00:00",
            "is_active": True
        }

        mock_insert_result = AsyncMock()
        mock_insert_result.inserted_id = "68e68a4025035785b7c93f3f"

        with patch("service.job_posting_service.db") as mock_db:
            mock_db.jobs.find_one = AsyncMock(return_value=None)
            mock_db.jobs.insert_one = AsyncMock(return_value=mock_insert_result)

            response = client.post("/v1/jobs", json=job_payload)
            assert response.status_code == 200
            data = response.json()
            assert data["_id"] == "68e68a4025035785b7c93f3f"
            assert data["title"] == "Backend Developer"
            assert data["user_id"] == "123"


    def test_create_job_posting_already_exists(self,client):
        job_payload = {
            "user_id": "123",
            "title": "Backend Developer",
            "description": "Build APIs and service",
            "company": "Zaptide",
            "location": "Hyderabad",
            "salary": 1200000.0,
            "posted_date": "2025-10-08T12:00:00",
            "is_active": True
        }

        with patch("service.job_posting_service.db") as mock_db:
            mock_db.jobs.find_one = AsyncMock(return_value=mock_job)

            response = client.post("/v1/jobs", json=job_payload)
            assert response.status_code == 400
            assert response.json()["detail"] == "Job already exists"


    def test_get_job_by_id_success(self,client):
        job_id = "68e68a4025035785b7c93f3f"

        with patch("controllers.v1.job_posting_controller.db") as mock_db:
            mock_db.jobs.find_one = AsyncMock(return_value=mock_job)

            response = client.get(f"/v1/jobs/{job_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["_id"] == job_id
            assert data["title"] == "Backend Developer"
            assert data["user_id"] == "123"


    def test_get_job_by_id_not_found(self,client):
        job_id = "68e68a4025035785b7c93f3a"

        with patch("controllers.v1.job_posting_controller.db") as mock_db:
            mock_db.jobs.find_one = AsyncMock(return_value=None)

            response = client.get(f"/v1/jobs/{job_id}")
            assert response.status_code == 404

    def test_update_job_posting_success(self,client):
        job_id = "68e68a4025035785b7c93f3f"
        update_payload = {
            "title": "Senior Backend Developer",
            "salary": 1300000.0
        }

        updated_job = mock_job.copy()
        updated_job.update(update_payload)

        with patch("service.job_posting_service.db") as mock_db:
            mock_db.jobs.find_one = AsyncMock(side_effect=[mock_job, updated_job])
            mock_db.jobs.update_one = AsyncMock()

            response = client.patch(f"/v1/jobs/{job_id}", json=update_payload)
            assert response.status_code == 204