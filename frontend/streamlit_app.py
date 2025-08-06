import streamlit as st
import requests

st.title("ResumeGPT")
job_desc = st.text_area("Job Description")
if st.button("Generate Cover Letter"):
    resp = requests.get(
        "http://localhost:8000/cover-letter", params={"job_desc": job_desc}
    )
    st.write(resp.json().get("cover_letter", "No response"))
