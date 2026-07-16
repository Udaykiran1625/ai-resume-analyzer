from flask import Flask, request, jsonify
from flask_cors import CORS

from extractor import extract_text
from section_parser import parse_sections
from ats_scorer import compute_overall_score
from insights_generator import generate_insights

app = Flask(__name__)
CORS(app)  # allows the React app (different port) to call this API


@app.route("/api/health", methods=["GET"])
def health_check():
    """Simple endpoint to confirm the server is alive."""
    return jsonify({"status": "ok", "message": "Backend is running"})


@app.route("/api/analyze", methods=["POST"])
def analyze_resume():
    # 1. Check a file was actually sent
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    # 2. Optional job description, sent as regular form data
    jd_text = request.form.get("job_description", "")

    try:
        # 3. Run the full pipeline
        text = extract_text(file)

        if not text.strip():
            return jsonify({"error": "Could not extract any text from this PDF. It might be a scanned image."}), 400

        sections = parse_sections(text)
        scores = compute_overall_score(text, sections, jd_text=jd_text)
        insights = generate_insights(scores, sections, jd_text=jd_text)

        return jsonify({
            "sections": sections,
            "scores": scores,
            "insights": insights,
        })

    except Exception as e:
        return jsonify({"error": f"Something went wrong while analyzing the resume: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)