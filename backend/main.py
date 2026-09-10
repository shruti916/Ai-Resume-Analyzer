import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from backend.utils.parser import extract_text_from_pdf
from backend.utils.matcher import compute_similarity

app = FastAPI(title="AI Resume Analyzer", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_text: str = Form(...)
):
    # save to temp file so pdfplumber can read
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # extract text
    if suffix.lower() == ".pdf":
        resume_text = extract_text_from_pdf(tmp_path)
    else:
        with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
            resume_text = f.read()

    # compute similarity
    result = compute_similarity(resume_text, job_text)

    # cleanup temp
    os.remove(tmp_path)

    return {
        "filename": file.filename,
        "score": result["score"],
        "missing_keywords": result["missing_keywords"]
    }
