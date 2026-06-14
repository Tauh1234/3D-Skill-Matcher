from fastapi import FastAPI
from pydantic import BaseModel
from backend.matcher import match_skills   # ✅ ध्यान दो: backend.matcher नहीं, सिर्फ matcher

app = FastAPI()

class ResumeData(BaseModel):
    resume_text: str
    job_role: str
    required_skills: str
    user_skills: str

@app.get("/")  
def read_root():
    return {"message": "Backend running successfully"}

@app.post("/match")
def match_resume(data: ResumeData):
    resume_skills = [word.strip().lower() for word in data.user_skills.split(",")]
    job_skills = [word.strip().lower() for word in data.required_skills.split(",")]
    result = match_skills(resume_skills, job_skills)
    return result
