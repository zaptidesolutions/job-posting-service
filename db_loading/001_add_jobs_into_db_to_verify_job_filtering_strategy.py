# seed_jobs.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
db_url = "mongodb://localhost:27017"
db_name = "freelance_details"
collection_name = "jobs"

NUM_RECORDS = 5000  # number of jobs you want to insert
SKILLS = ["Python", "Java", "React", "Angular", "Django", "Spring Boot", "AWS", "Docker"]

async def seed_jobs():
    client = AsyncIOMotorClient(db_url)
    db = client[db_name]
    jobs_collection = db[collection_name]

    job_docs = []
    for _ in range(NUM_RECORDS):
        posted_days_ago = random.randint(0, 30)
        job_doc = {
            "user_id": fake.uuid4(),
            "title": fake.job(),
            "description": fake.text(max_nb_chars=200),
            "company": fake.company(),
            "location": fake.city(),
            "salary": round(random.uniform(50000, 2000000), 2),
            "posted_date": datetime.utcnow() - timedelta(days=posted_days_ago),
            "is_active": True,
            "skills": random.sample(SKILLS, k=random.randint(1, 4))
        }
        job_docs.append(job_doc)

    result = await jobs_collection.insert_many(job_docs)
    print(f"Inserted {len(result.inserted_ids)} jobs into the DB")
    client.close()

asyncio.run(seed_jobs())