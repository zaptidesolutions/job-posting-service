from JobQueryStrategy import JobQueryStrategy
class RecentJobStrategy(JobQueryStrategy):
    def apply(self, query: dict, sort: list):
        # Just sort by posted_date descending (recent first)
        return query, [("posted_date", -1)]
