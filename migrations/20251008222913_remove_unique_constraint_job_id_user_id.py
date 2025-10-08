from mongo_migrate.base_migrate import BaseMigration
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
freelance_db = client["freelance_details"]

## Used it to run the downgrade migration to remove the unique constraint

class Migration(BaseMigration):
    def upgrade(self):
        # MongoDB automatically names the index based on the fields and directions:
        freelance_db.jobs.drop_index("job_id_1_user_id_1")
        
    def downgrade(self):
        pass

    def comment(self):
        return 'Revoking the previous constraint'
    