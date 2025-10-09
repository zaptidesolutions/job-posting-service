from fastapi import APIRouter, Query
from service.job_list_service import JobListService
from models.JobInfo import JobInfo
from service.job_filtering_strategy.SkillJobFilter import SkillJobFilter
from service.job_filtering_strategy.RecentJobFilter import RecentJobFilter


router = APIRouter()
@router.get("/v2/jobs/search-by", response_model=list[JobInfo])
async def list_jobs(
    page: int = 1,
    page_size: int = 20,
    days: int = Query(7, description="Recent posts in last X days"),
    skills: list[str] = Query(None, description="Filter by required skills")
):
    if skills:
        strategy = SkillJobFilter(required_skills=skills)
    else:
        strategy = RecentJobFilter(days=days)

    jobs = await JobListService().get_jobs(strategy, page, page_size)
    return jobs