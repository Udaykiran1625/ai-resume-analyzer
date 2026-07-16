import { useState } from "react";
import { analyzeResume } from "./api";
import "./App.css";

function ScoreBar({ label, value }) {
  return (
    <div className="score-breakdown-row">
      <div className="score-breakdown-label">
        <span>{label}</span>
        <span>{value}%</span>
      </div>
      <div className="score-bar-track">
        <div className="score-bar-fill" style={{ width: `${value}%` }}></div>
      </div>
    </div>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select a PDF resume first.");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeResume(file, jobDescription);
      setResult(data);
    } catch (err) {
      setError("Something went wrong while analyzing the resume. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">AI Resume Analyzer</h1>
      <p className="app-subtitle">Upload your resume and get an instant ATS-style breakdown</p>

      <div className="card">
        <label className="field-label">Upload your resume (PDF only)</label>
        <input type="file" accept=".pdf" onChange={handleFileChange} />

        <div style={{ marginTop: "20px" }}>
          <label className="field-label">Job description (optional)</label>
          <textarea
            rows={5}
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste a job description here to get keyword match scoring..."
          />
        </div>

        <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {error && <p className="error-text">{error}</p>}
      </div>

      {result && (
        <>
          <div className="card overall-score">
            <div className="score-number">{result.scores.overall_score}%</div>
            <p className="summary-text">{result.insights.summary}</p>
          </div>

          <div className="card">
            <h3 className="section-heading">Score Breakdown</h3>
            <ScoreBar label="Skills" value={result.scores.skills_score} />
            <ScoreBar label="Structure" value={result.scores.structure_score} />
            <ScoreBar label="Project Detail" value={result.scores.project_score} />
            {result.scores.keyword_score !== null && (
              <ScoreBar label="Job Match" value={result.scores.keyword_score} />
            )}
          </div>

          <div className="two-column">
            <div className="card">
              <h3 className="section-heading">Strengths</h3>
              <ul className="insight-list">
                {result.insights.strengths.map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>

            <div className="card">
              <h3 className="section-heading">Weaknesses</h3>
              <ul className="insight-list">
                {result.insights.weaknesses.length > 0
                  ? result.insights.weaknesses.map((w, i) => <li key={i}>{w}</li>)
                  : <li>None detected</li>}
              </ul>
            </div>
          </div>

          <div className="card">
            <h3 className="section-heading">Suggestions</h3>
            <ul className="insight-list">
              {result.insights.suggestions.length > 0
                ? result.insights.suggestions.map((s, i) => <li key={i}>{s}</li>)
                : <li>None needed</li>}
            </ul>
          </div>

          <div className="card">
            <h3 className="section-heading">Sample Interview Questions</h3>
            <ul className="insight-list">
              {result.insights.interview_questions.map((q, i) => <li key={i}>{q}</li>)}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}

export default App;