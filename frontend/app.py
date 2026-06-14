import streamlit as st
import requests
import fitz  # PyMuPDF

st.title("⚡ Skill Matcher Agent")

# User Details
name = st.text_input("Your Name", key="name")
email = st.text_input("Email", key="email")
skills_input = st.text_area("resume skills (comma separated)", key="skills_input")

# Resume Upload
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="resume")

# Store resume text in session_state
if uploaded_file is not None and "resume_text" not in st.session_state:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    resume_text = ""
    for page in doc:
        resume_text += page.get_text()
    st.session_state["resume_text"] = resume_text
    st.success("✅ Resume Uploaded Successfully!")

# Skill Match Section
st.subheader("⚡ Skill Match")
required_skills = st.text_area("Required skills", "python,sql,machine learning,tensorflow", key="required_skills")

if st.button("Match Skills"):
    if "resume_text" not in st.session_state:
        st.warning("Please upload a resume first.")
    else:
        response = requests.post(
            "http://127.0.0.1:8000/match",
            json={
                "resume_text": st.session_state["resume_text"],
                "job_role": "Custom",
                "required_skills": required_skills,
                "user_skills": skills_input
            }
        )
        result = response.json()
        st.write("Matched Skills:", result["matched"])
        st.write("Score:", f"{result['score']}%")
