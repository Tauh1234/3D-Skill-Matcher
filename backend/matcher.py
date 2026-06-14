def match_skills(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)
    matched = resume_set.intersection(job_set)
    return {
        "matched": list(matched),
        "score": round(len(matched) / len(job_set) * 100, 2) if job_set else 0
    }
