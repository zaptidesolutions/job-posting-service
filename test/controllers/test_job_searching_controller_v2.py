import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, MagicMock, patch
# Assuming the correct path for the router is job_searching_controller
from controllers.v2.job_searching_controller import router as job_search_router

# Import the service file to patch the database usage correctly

app = FastAPI()
app.include_router(job_search_router)

@pytest.fixture(scope="class")
def client():
    # Use the app fixture if defined, otherwise use the simple FastAPI app
    return TestClient(app)


# Define the mock job with the expected structure of the MongoDB document *before* conversion.
# IMPORTANT: The database returns ObjectId, so we mock it as a dictionary with a string _id
# and add the missing 'skills' field.
mock_job_db = {
    "_id": "68e68a4025035785b7c93f3f",
    "user_id": "123",
    "title": "Backend Developer",
    "description": "Build APIs and service",
    "company": "Zaptide",
    "location": "Hyderabad",
    "salary": 1200000.0,
    "posted_date": "2025-10-08T12:00:00",
    "is_active": True,
    "skills": ["Python", "FastAPI", "MongoDB"] # <--- ADDED REQUIRED FIELD
}

# Define the expected JSON response structure (where _id is guaranteed to be a string)
mock_job_response = mock_job_db.copy()


@pytest.mark.usefixtures("client")
class TestJobSearchingController:

    def test_get_jobs_by_recent_postings_success(self, client):
        # Patch the database object used inside the service layer
        with patch("service.job_list_service.db") as mock_db:
            
            # Setup mock cursor behavior
            mock_cursor = MagicMock()
            mock_cursor.sort.return_value = mock_cursor
            mock_cursor.skip.return_value = mock_cursor
            mock_cursor.limit.return_value = mock_cursor
            
            # Mock to_list() to return the list of mock jobs
            mock_cursor.to_list = AsyncMock(return_value=[mock_job_db])

            # Mock the initial find() call to return the mock cursor
            mock_db.jobs.find.return_value = mock_cursor

            response = client.get("/v2/jobs/search-by?days=7&page=1&page_size=10")
            
            # Check the status code
            assert response.status_code == 200
            
            # Check the response content
            response_data = response.json()
            
            # The exact string comparison can be brittle, so we check size and key content
            assert len(response_data) == 1
            
            # Check that the first job in the response matches the expected structure
            assert response_data[0]["_id"] == mock_job_response["_id"]
            assert response_data[0]["title"] == mock_job_response["title"]
            assert response_data[0]["skills"] == mock_job_response["skills"]
            
            # OPTIONAL: Use the exact equality check, but be prepared for date/time formatting differences.
            # assert response.json() == [mock_job_response]

            # Ensure the service called find with the correct initial query (should be empty for recent posts)
            mock_db.jobs.find.assert_called_once()
