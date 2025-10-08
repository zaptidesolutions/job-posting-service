from .JobStrategy import JobFilterStrategy
from datetime import datetime, timedelta
class RecentJobFilter(JobFilterStrategy):
    def __init__(self, days: int = 7):  # default to last 7 days
        self.days = days

    def build_query(self):
        cutoff_date = datetime.utcnow() - timedelta(days=self.days)
        return {"posted_date": {"$gte": cutoff_date}}

    def build_sort(self):
        return [("posted_date", -1)]
