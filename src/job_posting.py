from fastapi import FastAPI
from controllers.v1.job_posting_controller import router as job_router
from controllers.v1.job_searching_controller import router as job_search_router
api = FastAPI(title="Job Posting Service")

api.include_router(job_router)
api.include_router(job_search_router)