from fastapi import APIRouter, HTTPException, Body,status
from models.user_applied_job import UserAppliedJob
from bson import ObjectId
from config.db_config import freelance_db as db

router = APIRouter()

# ---------------- Job Applying Endpoints ----------------
@router.post("/v1/jobs/apply", status_code=status.HTTP_201_CREATED)
async def apply_to_job(application: UserAppliedJob = Body(...)):