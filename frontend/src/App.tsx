import { useState } from "react";
import axios from "axios";
import {
  TextField,
  Button,
  LinearProgress,
  Box,
} from "@mui/material";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !jobText) {
      alert("Upload a resume and paste a job ad!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_text", jobText);

    try {
      setLoading(true);
      const res = await axios.post("http://127.0.0.1:8000/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Error analyzing resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h1>AI Resume Analyzer</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf,.txt"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          style={{ margin: "20px 0" }}
        />
        <TextField
          label="Paste Job Description"
          multiline
          fullWidth
          rows={4}
          value={jobText}
          onChange={(e) => setJobText(e.target.value)}
        />
        <Button type="submit" variant="contained" sx={{ mt: 2 }}>
          Analyze
        </Button>
      </form>

      {loading && <LinearProgress sx={{ mt: 2 }} />}

      {result && (
        <>
          <h2>Result</h2>
          <p><strong>Filename:</strong> {result.filename}</p>
          <p><strong>Match Score:</strong> {result.score}%</p>

          {/* Progress Bar */}
          <Box sx={{ width: "100%", mb: 2 }}>
            <LinearProgress
              variant="determinate"
              value={result.score}
              sx={{
                height: 12,
                borderRadius: 6,
                backgroundColor: "#e5e7eb",
                "& .MuiLinearProgress-bar": {
                  backgroundColor:
                    result.score >= 70
                      ? "#22c55e" // green
                      : result.score >= 40
                      ? "#f59e0b" // orange
                      : "#ef4444", // red
                },
              }}
            />
          </Box>

          <p><strong>Missing Keywords:</strong></p>
          <div>
            {result.missing_keywords.map((word: string, i: number) => (
              <span key={i} className="result-badge">{word}</span>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;
