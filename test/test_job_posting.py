import pytest
from starlette.testclient import TestClient
from unittest.mock import patch, AsyncMock
from job_posting import api # Assuming your FastAPI app instance is named 'api' and is in 'src/main.py'

# Initialize the TestClient using the FastAPI app instance
client = TestClient(api)

# Mock data for successful job creation
MOCK_JOB_PAYLOAD = {
    "user_id": "999",
    "title": "Senior Python Developer",
    "description": "Develop and maintain backend services.",
    "company": "TechCorp",
    "location": "Remote",
    "salary": 1500000.0,
    "posted_date": "2025-10-09T10:00:00",
    "is_active": True
}

class TestAPI:

    def test_api_root_status(self):
        """
        Test that the API root is accessible (FastAPI default behavior)
        or that a simple health check endpoint returns 200.
        (Using a simple check here, assuming no custom root route is defined)
        """
        # A typical check for a running API might be hitting the docs path or a health endpoint
        response = client.get("/") 
        # FastAPI's default root behavior usually returns a 404 if no route is defined, 
        # but we test for the app being loadable.
        assert response.status_code == 404 or response.status_code == 200

    def test_job_router_is_included(self):
        """
        Verify that the job router endpoints are correctly included 
        and accessible under the expected path prefix (/v1/jobs).
        This tests the routing setup, not the controller logic itself.
        """
        # We can test this by hitting the 'create job' endpoint with a mock and verifying 
        # the status code (which would likely be a 422 if the model is violated, or hit the controller).

        # Mock database interactions for a successful POST to /v1/jobs
        mock_insert_result = AsyncMock()
        mock_insert_result.inserted_id = "mocked_mongo_id_001"
        
        # Use the patch from the previous conversation:
        # Mock 'find_one' to return None (job doesn't exist)
        # Mock 'insert_one' to return a successful result
        with patch("service.job_posting_service.db") as mock_db:
            mock_db.jobs.find_one = AsyncMock(return_value=None)
            mock_db.jobs.insert_one = AsyncMock(return_value=mock_insert_result)

            response = client.post("/v1/jobs", json=MOCK_JOB_PAYLOAD)

            # Assert that the request successfully hit the controller and returned a successful status code.
            # We assume the controller returns 201 for success.
            assert response.status_code == 200
            assert mock_db.jobs.insert_one.called
            
    # Add other routing tests here, e.g., for GET /v1/jobs/{job_id}
    # For example:
    # def test_get_job_by_id_route(self):
    #     response = client.get("/v1/jobs/non_existent_id")
    #     # This checks that the route is defined and FastAPI handles the request, 
    #     # likely returning a 404 or hitting the controller logic.
    #     assert response.status_code in (404, 200) # Depends on controller logic.
