from JobQueryStrategy import JobQueryStrategy
class SkillJobStrategy(JobQueryStrategy):
    def __init__(self, skills: list[str]):
        self.skills = skills

    def apply(self, query: dict, sort: list):
        query["skills"] = {"$in": self.skills}
        return query, sort
