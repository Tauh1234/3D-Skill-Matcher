import streamlit as st
import requests
import fitz  # PyMuPDF

st.title("⚡ Skill Matcher Agent")

# User Details
name = st.text_input("Your Name", key="name")
email = st.text_input("Email", key="email")
skills_input = st.text_area(
    "Resume Skills (comma separated)",
    key="skills_input"
)

# Resume Upload
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"],
    key="resume"
)

# Store resume text
if uploaded_file is not None and "resume_text" not in st.session_state:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    resume_text = ""
    for page in doc:
        resume_text += page.get_text()

    st.session_state["resume_text"] = resume_text
    st.success("✅ Resume Uploaded Successfully!")

# Skill Match Section
st.subheader("⚡ Skill Match")

required_skills = st.text_area(
    "Required Skills",
    "python,sql,machine learning,tensorflow",
    key="required_skills"
)

if st.button("Match Skills"):
    if "resume_text" not in st.session_state:
        st.warning("Please upload a resume first.")
    else:
        try:
            response = requests.post(
                "https://threed-skill-matcher-1.onrender.com/match",
                json={
                    "resume_text": st.session_state["resume_text"],
                    "job_role": "Custom",
                    "required_skills": required_skills,
                    "user_skills": skills_input
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()

                st.success("✅ Matching Completed")

                st.write("### Matched Skills")
                st.write(result.get("matched", []))

                st.write("### Match Score")
                st.write(f"{result.get('score', 0)}%")

            else:
                st.error(
                    f"API Error: {response.status_code}"
                )

        except Exception as e:
            st.error(f"Connection Error: {e}")