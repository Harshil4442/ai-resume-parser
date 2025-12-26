import json
from pathlib import Path
from typing import List, Dict

COURSES_PATH = Path(__file__).parent.parent.parent / "resources" / "courses.json"

with open(COURSES_PATH, encoding="utf-8") as f:
    COURSES = json.load(f)

def recommend_for_gaps(missing_skills: List[str], weeks: int = 4) -> List[Dict]:
    missing_set = set(missing_skills)
    scored = []

    for course in COURSES:
        course_skills = set(course.get("skills", []))
        overlap = len(missing_set & course_skills)
        if overlap == 0:
            continue

        level_weight = {"beginner": 1.5, "intermediate": 1.0, "advanced": 0.5}.get(
            course.get("level", "intermediate"), 1.0
        )
        score = overlap * level_weight
        scored.append((score, course))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored]
