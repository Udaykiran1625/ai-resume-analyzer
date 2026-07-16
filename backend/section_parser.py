import re

SECTION_HEADERS = {
    "skills": r"(technical\s+skills|skills|core\s+competencies)",
    "education": r"(education|academic\s+background|qualifications)",
    "experience": r"(experience|work\s+experience|internship|professional\s+experience)",
    "projects": r"(projects|academic\s+projects|personal\s+projects)",
    "certifications": r"(certifications|certificates|licenses)",
}

BULLET_CHARS = ("•", "●", "-", "*", "○", "◦")


def is_probable_header(line):
    """
    A real header line is short and doesn't start with a bullet symbol.
    This stops us from mistaking bullet content (or wrapped sentences
    that happen to mention 'education' or 'projects') for a real header.
    """
    if not line:
        return False
    if line.startswith(BULLET_CHARS):
        return False
    word_count = len(line.split())
    if word_count > 6:
        return False
    return True


def parse_sections(text):
    lines = text.split("\n")
    sections = {key: [] for key in SECTION_HEADERS}
    current_section = None

    for line in lines:
        stripped = line.strip()
        matched_header = False

        if is_probable_header(stripped):
            for key, pattern in SECTION_HEADERS.items():
                # Match at the START of the line (not the whole line),
                # so "PROJECTS / RESEARCH" still counts as "projects".
                if re.match(rf"^\s*{pattern}\b", stripped, re.IGNORECASE):
                    current_section = key
                    matched_header = True
                    break

        if not matched_header and current_section:
            if stripped:
                sections[current_section].append(stripped)

    return {k: "\n".join(v).strip() for k, v in sections.items()}