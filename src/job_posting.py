from fastapi import FastAPI
from controllers.v1.job_posting_controller import router as job_router
api = FastAPI(title="Job Posting Service")

api.include_router(job_router)