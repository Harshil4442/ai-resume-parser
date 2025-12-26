from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..services.parsing import parse_resume_file

router = APIRouter(prefix="/resume", tags=["resume"])

@router.post("/parse", response_model=schemas.ResumeParseResponse)
async def parse_resume(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed = {"application/pdf", "application/octet-stream", "application/x-pdf"}
    if (file.content_type or "") not in allowed:
        raise HTTPException(status_code=400, detail=f"Only PDF supported. content_type={file.content_type}")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file upload.")

    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            db.add(models.User(id=user_id, email=f"demo+{user_id}@local", password_hash=""))
            db.commit()

        raw_text, sections, skills, exp_years = parse_resume_file(file_bytes)

        resume = models.Resume(
            user_id=user_id,
            original_filename=file.filename or "",
            raw_text=raw_text,
            skills=skills,
            experience_years=exp_years,
            sections=sections,
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)

        return schemas.ResumeParseResponse(
            resume_id=resume.id,
            skills=skills,
            experience_years=exp_years,
            sections=sections,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
