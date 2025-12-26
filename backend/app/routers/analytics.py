from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
async def analytics_summary(user_id: int, db: Session = Depends(get_db)):
    resumes = db.query(models.Resume).filter_by(user_id=user_id).all()
    job_matches = db.query(models.JobMatch).filter_by(user_id=user_id).all()

    total_skills = len(set(s for r in resumes for s in (r.skills or [])))
    avg_match = (
        sum(jm.match_score for jm in job_matches) / len(job_matches)
        if job_matches else 0.0
    )

    history = [
        {"timestamp": jm.created_at.isoformat(), "match_score": jm.match_score}
        for jm in job_matches
    ]

    return {
        "profile_completeness": min(100, total_skills * 3),
        "avg_match_score": avg_match,
        "applications_count": len(job_matches),
        "match_history": history,
    }
