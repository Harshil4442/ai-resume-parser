from fastapi import APIRouter
from typing import List
from ..services.recommender import recommend_for_gaps

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("/gaps")
async def gaps_and_recommendations(missing_skills: List[str]):
    roadmap = recommend_for_gaps(missing_skills)
    return {"missing_skills": missing_skills, "roadmap": roadmap}
