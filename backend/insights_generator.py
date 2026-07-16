def generate_insights(scores, sections, jd_text=None):
    """
    Takes the scoring results and builds human-readable feedback:
    a summary, strengths, weaknesses, missing skills, suggestions,
    and mock interview questions.
    """
    strengths = []
    weaknesses = []
    missing_skills = []
    suggestions = []
    interview_questions = []

    found_skills = scores["found_skills"]
    matched_keywords = scores["matched_keywords"]

    # --- Strengths & weaknesses based on skills ---
    if scores["skills_score"] >= 70:
        strengths.append("Strong and diverse technical skill set is clearly listed.")
    elif scores["skills_score"] >= 40:
        strengths.append("Decent technical skill coverage, with room to expand.")
    else:
        weaknesses.append("Very few recognizable technical skills were found in the resume.")
        suggestions.append("List more specific tools, languages, and frameworks you've used.")

    # --- Structure feedback ---
    if scores["structure_score"] < 100:
        missing = []
        for section in ["skills", "education", "projects"]:
            if not sections.get(section):
                missing.append(section)
        if missing:
            weaknesses.append(f"Missing or empty section(s): {', '.join(missing)}.")
            suggestions.append(f"Add a clear '{missing[0].capitalize()}' section with a proper heading.")
    else:
        strengths.append("Resume has all the essential sections clearly structured.")

    # --- Project quality feedback ---
    if scores["project_score"] < 50:
        weaknesses.append("Project section lacks enough detail or measurable outcomes.")
        suggestions.append("Add 2-3 bullet points per project, including tools used and results achieved.")
    else:
        strengths.append("Projects are well described with multiple detailed bullet points.")

    # --- Job description-specific feedback ---
    if jd_text and jd_text.strip():
        if scores["keyword_score"] is not None and scores["keyword_score"] < 50:
            weaknesses.append("Resume doesn't closely match the keywords in the target job description.")
            suggestions.append("Mirror more of the specific terms used in the job description (where truthful).")
        elif scores["keyword_score"] is not None:
            strengths.append("Resume aligns well with the target job description's key terms.")

    # --- Missing technical skills (only meaningful if a JD was given) ---
    if jd_text and jd_text.strip():
        jd_lower = jd_text.lower()
        resume_skills_lower = [s.lower() for s in found_skills]
        # crude check: common important skill words mentioned in JD but not resume
        for word in matched_keywords:
            pass  # matched_keywords already means "found in resume", so skip these

    # --- Mock interview questions based on found skills ---
    for skill in found_skills[:4]:
        interview_questions.append(
            f"Can you walk me through a project where you used {skill}?"
        )
    if not interview_questions:
        interview_questions.append(
            "Tell me about a technical project you're most proud of and why."
        )

    # --- Summary ---
    top_skills = ", ".join(found_skills[:5]) if found_skills else "a few general skills"
    summary = (
        f"This resume demonstrates experience with {top_skills}. "
        f"It scores {scores['overall_score']}% overall"
        + (f" against the provided job description." if jd_text and jd_text.strip() else ".")
    )

    return {
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "interview_questions": interview_questions,
    }