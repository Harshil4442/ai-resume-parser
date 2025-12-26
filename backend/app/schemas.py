from pydantic import BaseModel
from typing import List, Optional, Dict

class ResumeParseResponse(BaseModel):
    resume_id: int
    skills: List[str]
    experience_years: float
    sections: Dict[str, str]

class JobMatchRequest(BaseModel):
    user_id: int
    resume_id: int
    job_title: str
    company: Optional[str] = None
    job_description: str

class JobMatchResponse(BaseModel):
    match_id: int
    match_score: float
    required_skills: List[str]
    missing_skills: List[str]
    weak_skills: List[str]

class RewriteBulletsRequest(BaseModel):
    resume_id: int
    job_description: str
    tone: str = "concise"

class RewriteBulletsResponse(BaseModel):
    rewritten_bullets: List[str]
    summary: str

class InterviewQuestionsRequest(BaseModel):
    job_title: str
    job_description: str

class InterviewQuestionsResponse(BaseModel):
    questions: List[Dict[str, str]]  # {question, answer}
