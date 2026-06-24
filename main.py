from fastapi import FastAPI, UploadFile, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from app.parser import extract_text_from_pdf
from app.scorer import analyze_resume_vs_jd
from app.generator import build_ats_friendly_pdf
import json

app = FastAPI(title="Professional ATS Pipeline Suite")

# Configure CORS so your React frontend can talk to your FastAPI backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/score")
async def score_resume_endpoint(file: UploadFile = File(...), job_description: str = Form(...)):
    try:
        file_bytes = await file.read()
        # Call parser module
        resume_text = extract_text_from_pdf(file_bytes)
        # Call scoring module
        analysis_result = analyze_resume_vs_jd(resume_text, job_description)
        return {"status": "success", "data": analysis_result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/v1/generate")
async def generate_resume_endpoint(payload: str = Form(...)):
    try:
        data = json.loads(payload)
        # Call generator module to build PDF stream
        pdf_stream = build_ats_friendly_pdf(data)
        return Response(
            content=pdf_stream.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=ats_perfect_resume.pdf"}
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}