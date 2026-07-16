from extractor import extract_text
from section_parser import parse_sections
from ats_scorer import compute_overall_score
from insights_generator import generate_insights

with open("sample_resume.pdf", "rb") as f:
    text = extract_text(f)

sections = parse_sections(text)

sample_jd = """
We are looking for a Software Engineer with strong skills in Python,
React.js, Flask, REST API design, and SQL databases. Experience with
Git, Docker, and cloud platforms like AWS is a plus. Familiarity with
data structures and algorithms is required.
"""

scores = compute_overall_score(text, sections, jd_text=sample_jd)
insights = generate_insights(scores, sections, jd_text=sample_jd)

print("=== SCORES ===")
for k, v in scores.items():
    print(f"{k}: {v}")

print("\n=== INSIGHTS ===")
for k, v in insights.items():
    print(f"{k}: {v}")