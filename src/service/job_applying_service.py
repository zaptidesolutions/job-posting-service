from config.db_config import freelance_db as db
from models.user_applied_job import UserAppliedJob
from fastapi import HTTPException

async def apply_to_job(application: UserAppliedJob):
    existing_application = await db.applications.find_one({
        "user_id": application.user_id,
        "job_id": application.job_id
    })
    
    if existing_application:
        raise HTTPException(status_code=400, detail="Application already exists")
    
    application_dict = application.dict()
    inserted_record = await db.applications.insert_one(application_dict)
    
    # Convert ObjectId to string
    application_dict["_id"] = str(inserted_record.inserted_id)
    
    return application_dict