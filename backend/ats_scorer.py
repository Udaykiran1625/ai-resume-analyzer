import json
import re
import os

# Find the exact path to skills_db.json, no matter where this script is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_PATH = os.path.join(BASE_DIR, "data", "skills_db.json")

with open(SKILLS_PATH) as f:
    SKILL_CATEGORIES = json.load(f)

# Flatten all categories (languages, frontend, backend, etc.) into one big list
ALL_SKILLS = []
for category_skills in SKILL_CATEGORIES.values():
    ALL_SKILLS.extend(category_skills)

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "you", "your", "are",
    "will", "have", "has", "our", "from", "who", "job", "role", "team",
    "work", "experience", "years", "year", "ability", "strong", "must",
    "should", "into", "such", "using", "able", "well", "role", "including",
    "including", "candidate", "candidates", "responsibilities", "requirements"
}


def score_skills(text):
    """
    Checks how many known technical skills from skills_db.json
    appear anywhere in the resume text.
    """
    text_lower = text.lower()
    found = [skill for skill in ALL_SKILLS if skill in text_lower]
    # We cap the score at 15 matched skills = 100%, so having way more
    # than 15 doesn't matter - it's about solid coverage, not padding.
    score = min(len(found) / 15, 1) * 100
    return round(score, 2), found


def score_structure(sections):
    """
    Checks whether the essential resume sections are present at all.
    """
    required = ["skills", "education", "projects"]
    present = [s for s in required if sections.get(s)]
    return round(len(present) / len(required) * 100, 2)


def score_projects(sections):
    """
    Crude but effective: counts bullet points in the Projects section.
    More bullets usually means more detailed, well-explained projects.
    """
    project_text = sections.get("projects", "")
    bullet_count = len(re.findall(r"[•●○◦\-\*]\s", project_text))
    return round(min(bullet_count * 10, 100), 2)


def extract_keywords_from_jd(jd_text):
    """
    Pulls meaningful keywords out of a pasted job description,
    ignoring common filler words like 'the', 'and', 'experience'.
    """
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9\.\+#]*", jd_text.lower())
    keywords = [w for w in words if len(w) > 3 and w not in STOPWORDS]

    # Remove duplicates while keeping the original order
    seen = set()
    unique_keywords = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            unique_keywords.append(w)
    return unique_keywords


def score_keywords(text, jd_text):
    """
    Compares the resume against a job description's keywords.
    Returns None if no job description was provided (this is optional).
    """
    if not jd_text or not jd_text.strip():
        return None, []

    text_lower = text.lower()
    keywords = extract_keywords_from_jd(jd_text)
    if not keywords:
        return 0, []

    matched = [k for k in keywords if k in text_lower]
    score = round(len(matched) / len(keywords) * 100, 2)
    return score, matched


def compute_overall_score(text, sections, jd_text=None):
    """
    Combines all individual scores into one overall ATS score,
    using different weightings depending on whether a job
    description was provided.
    """
    skills_score, found_skills = score_skills(text)
    structure_score = score_structure(sections)
    project_score = score_projects(sections)
    keyword_score, matched_keywords = score_keywords(text, jd_text)

    if keyword_score is not None:
        # A specific job was given, so keyword match matters a lot
        overall = round(
            skills_score * 0.30 +
            keyword_score * 0.30 +
            structure_score * 0.20 +
            project_score * 0.20, 2
        )
    else:
        # No job description, so lean more on general skill strength
        overall = round(
            skills_score * 0.45 +
            structure_score * 0.30 +
            project_score * 0.25, 2
        )

    return {
        "overall_score": overall,
        "skills_score": skills_score,
        "structure_score": structure_score,
        "project_score": project_score,
        "keyword_score": keyword_score,
        "found_skills": found_skills,
        "matched_keywords": matched_keywords,
    }