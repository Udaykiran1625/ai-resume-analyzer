# AI Resume Analyzer

A full-stack web application that analyzes PDF resumes and provides ATS-style scoring, section-by-section breakdown, and personalized improvement insights - including missing skills, strengths, weaknesses, and mock interview questions.

## Features

- **PDF Resume Parsing** - Extracts Skills, Education, Projects, Experience, and Certifications using rule-based regex parsing (no black-box ML).
- **ATS Scoring Engine** - Scores resumes based on technical skill coverage, resume structure, project detail, and (optionally) keyword match against a specific job description.
- **Personalized Insights** - Generates a summary, strengths, weaknesses, improvement suggestions, and sample interview questions based on detected skills.
- **Job Description Matching** - Paste a job description to get a tailored keyword-match score alongside the general resume score.
- **React Dashboard** - Clean, responsive UI with a live score breakdown, built with React and Vite.

## Tech Stack

**Frontend:** React.js, Vite, Axios
**Backend:** Flask, PDFPlumber, Python (regex-based parsing)

## How It Works

1. User uploads a PDF resume (and optionally pastes a job description) through the React frontend.
2. The file is sent via a REST API call to the Flask backend.
3. PDFPlumber extracts raw text from the PDF.
4. A regex-based parser splits the text into labeled sections (Skills, Education, Projects, etc.).
5. The scoring engine evaluates skill coverage, structure completeness, project detail, and job description keyword match.
6. An insights engine converts the scores into human-readable feedback and mock interview questions.
7. The full result is sent back to React and rendered as an interactive dashboard.

## Running Locally

### Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

Backend runs on http://127.0.0.1:5000

### Frontend
cd frontend
npm install
npm run dev

Frontend runs on http://127.0.0.1:5173

## Author

**Uday Kiran**
GitHub: https://github.com/Udaykiran1625
LinkedIn: https://www.linkedin.com/in/mekala-uday-kiran-8614533b1/
