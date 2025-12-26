from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..services.matching import extract_required_skills_from_jd, compute_match_score

router = APIRouter(prefix="/job", tags=["job"])

@router.post("/match", response_model=schemas.JobMatchResponse)
async def match_resume_to_job(payload: schemas.JobMatchRequest, db: Session = Depends(get_db)):
    resume = db.query(models.Resume).filter_by(id=payload.resume_id, user_id=payload.user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found. Upload and parse a resume first.")

    required_skills = extract_required_skills_from_jd(payload.job_description)
    score, missing, weak = compute_match_score(resume.skills or [], required_skills)

    jm = models.JobMatch(
        user_id=payload.user_id,
        resume_id=resume.id,
        job_title=payload.job_title,
        company=payload.company or "",
        job_description=payload.job_description,
        required_skills=required_skills,
        match_score=score,
        missing_skills=missing,
        weak_skills=weak,
    )
    db.add(jm)
    db.commit()
    db.refresh(jm)

    return schemas.JobMatchResponse(
        match_id=jm.id,
        match_score=score,
        required_skills=required_skills,
        missing_skills=missing,
        weak_skills=weak,
    )
