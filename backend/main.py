from fastapi import FastAPI
from pydantic import BaseModel
from matcher import match_skills

app = FastAPI()

class ResumeData(BaseModel):
    resume_text: str
    job_role: str
    required_skills: str
    user_skills: str

@app.post("/match")
def match_resume(data: ResumeData):
    resume_skills = [word.strip().lower() for word in data.user_skills.split(",")]
    job_skills = [word.strip().lower() for word in data.required_skills.split(",")]
    result = match_skills(resume_skills, job_skills)
    return result
