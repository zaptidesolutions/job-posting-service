from JobStrategy import JobFilterStrategy

class SkillJobFilter(JobFilterStrategy):
    def __init__(self, required_skills: list[str]):
        self.required_skills = required_skills
        
    def build_query(self):
        return {"skills": {"$in": self.required_skills}}

    def build_sort(self):
        return [("posted_date", -1)]
