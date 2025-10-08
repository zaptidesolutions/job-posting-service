from mongo_migrate.base_migrate import BaseMigration
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
freelance_db = client["freelance_details"]

class Migration(BaseMigration):
    def upgrade(self):
        """
        Creates a compound unique index on the 'jobs' collection, 
        ensuring that the combination of job_id and user_id is unique 
        across all documents.
        """
        # Index creation syntax: takes a list of (field, direction) tuples.
        # Direction 1 is ascending. The unique=True flag enforces the constraint.
        freelance_db.jobs.create_index(
            [("job_id", 1), ("user_id", 1)],
            unique=True
        )
        
    def downgrade(self):
        pass
        
    def comment(self):
        return 'create_job_id_and_user_id_compound_unique_index'
