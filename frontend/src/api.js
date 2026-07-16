import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";

export const analyzeResume = async (file, jobDescription) => {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("job_description", jobDescription || "");

  const response = await axios.post(`${API_BASE_URL}/api/analyze`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};