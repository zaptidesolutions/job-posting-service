from job_filtering_strategy.JobStrategy import JobFilterStrategy

class JobListService:
    def __init__(self, db):
        self.db = db

    async def get_jobs(self, strategy: JobFilterStrategy, page: int = 1, page_size: int = 20):
        skip = (page - 1) * page_size

        query = strategy.build_query()      # strategy-specific query
        sort = strategy.build_sort()        # strategy-specific sort

        cursor = self.db.jobs.find(query).sort(sort).skip(skip).limit(page_size)
        jobs = await cursor.to_list(length=page_size)
        return jobs