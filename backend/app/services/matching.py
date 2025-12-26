from typing import List, Tuple, Set
from sentence_transformers import SentenceTransformer, util
from .parsing import extract_skills

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_required_skills_from_jd(text: str) -> List[str]:
    return extract_skills(text)

def compute_match_score(resume_skills: List[str], jd_skills: List[str]) -> Tuple[float, List[str], List[str]]:
    set_resume: Set[str] = set(resume_skills)
    set_jd: Set[str] = set(jd_skills)

    missing = sorted(list(set_jd - set_resume))
    weak: List[str] = []  # future enhancement

    if not jd_skills:
        return 0.0, missing, weak

    resume_text = "; ".join(resume_skills) or "no skills"
    jd_text = "; ".join(jd_skills)

    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_jd = model.encode(jd_text, convert_to_tensor=True)

    sim = util.cos_sim(emb_resume, emb_jd).item()  # -1..1
    score = max(0.0, min(100.0, (sim + 1) * 50))   # map to 0..100

    return score, missing, weak
