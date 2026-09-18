import os
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

from src.resume_parser import extract_resume_text, extract_contact_info
from src.skill_extractor import load_skills
from src.analyzer import analyze_resume
from src.job_ranker import rank_jobs

BASE = Path(__file__).parent
DATA = BASE / "data"

st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide"
)

@st.cache_data
def load_data():
    jobs = pd.read_csv(DATA / "jobs.csv")
    skills = load_skills(DATA / "skills.csv")
    return jobs, skills

jobs_df, skills_df = load_data()

st.title("📄 AI-Powered Resume Analyzer & Job Matcher")
st.caption("NLP + Machine Learning • Resume analysis • Skill-gap detection • Job ranking")

with st.sidebar:
    st.header("How it works")
    st.write("1. Upload your resume")
    st.write("2. Extract and analyze resume content")
    st.write("3. Compare it with the job dataset")
    st.write("4. Rank jobs by relevance")
    st.write("5. Review matching and missing skills")
    st.divider()
    st.info("This demo uses TF-IDF cosine similarity, skill coverage, and experience alignment.")

uploaded = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx", "txt"],
    help="PDF, DOCX and TXT are supported."
)

if uploaded:
    try:
        resume_text = extract_resume_text(uploaded)
    except Exception as e:
        st.error(f"Could not read the resume: {e}")
        st.stop()

    if len(resume_text.strip()) < 30:
        st.warning("Very little text was extracted. If this is a scanned PDF, OCR may be required.")
        st.stop()

    st.success(f"Resume loaded: {uploaded.name}")

    contact = extract_contact_info(resume_text)
    analysis = analyze_resume(resume_text, skills_df)

    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🎯 Job Matches", "📝 Extracted Text"])

    with tab1:
        st.subheader("Resume overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Skills detected", len(analysis["skills"]))
        c2.metric("Experience detected", f"{analysis['experience_years']:.1f} yrs")
        c3.metric("Certifications", len(analysis["certifications"]))

        st.subheader("Contact information")
        st.write(f"**Email:** {contact['email'] or 'Not detected'}")
        st.write(f"**Phone:** {contact['phone'] or 'Not detected'}")
        if contact["links"]:
            st.write("**Links:** " + " • ".join(contact["links"]))

        st.subheader("Skills")
        if analysis["skills"]:
            st.write(" • ".join(analysis["skills"]))
        else:
            st.warning("No skills detected from the current skill dictionary.")

        st.subheader("Education")
        if analysis["education"]:
            for item in analysis["education"]:
                st.write(f"- {item}")
        else:
            st.write("No education entry detected.")

        st.subheader("Certifications")
        if analysis["certifications"]:
            for item in analysis["certifications"]:
                st.write(f"- {item}")
        else:
            st.write("No certifications detected.")

        if analysis["recommendations"]:
            st.subheader("Resume improvement suggestions")
            for item in analysis["recommendations"]:
                st.write(f"- {item}")

    with tab2:
        results = rank_jobs(resume_text, jobs_df, skills_df)

        st.subheader("Ranked job recommendations")
        display_df = results[["job_id", "title", "company", "location", "score"]].copy()
        display_df["score"] = (display_df["score"] * 100).round(1)
        display_df = display_df.rename(columns={"score": "match_score_%"})
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        chart_df = display_df.head(10).sort_values("match_score_%")
        fig = px.bar(
            chart_df,
            x="match_score_%",
            y="title",
            orientation="h",
            text="match_score_%",
            title="Top job matches"
        )
        fig.update_layout(xaxis_title="Match score (%)", yaxis_title="Job")
        st.plotly_chart(fig, use_container_width=True)

        selected_id = st.selectbox(
            "Inspect a job",
            results["job_id"].tolist(),
            format_func=lambda x: (
                results.loc[results["job_id"] == x, "title"].iloc[0]
                + " — "
                + results.loc[results["job_id"] == x, "company"].iloc[0]
            )
        )
        job = results.loc[results["job_id"] == selected_id].iloc[0]

        st.markdown(f"### {job['title']} — {job['company']}")
        a, b, c = st.columns(3)
        a.metric("Overall match", f"{job['score']*100:.1f}%")
        b.metric("Text similarity", f"{job['similarity']*100:.1f}%")
        c.metric("Skill coverage", f"{job['skill_coverage']*100:.1f}%")

        st.write(f"**Location:** {job['location']}")
        st.write(job["description"])

        left, right = st.columns(2)
        with left:
            st.subheader("✅ Matching skills")
            if job["matching_skills"]:
                for skill in job["matching_skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("No direct skill matches detected.")
        with right:
            st.subheader("⚠️ Skill gaps")
            if job["missing_skills"]:
                for skill in job["missing_skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("No skill gaps detected from the current dictionary.")

        st.subheader("Actionable insight")
        if job["missing_skills"]:
            st.info(
                "Focus on the missing skills above, then update your resume with "
                "projects, coursework, certifications, or experience that genuinely demonstrates them."
            )
        else:
            st.success("The resume contains the skills detected in this job description.")

    with tab3:
        st.text_area("Extracted resume text", resume_text, height=500)

else:
    st.info("Upload a resume to start the analysis.")
    st.subheader("Included dataset")
    st.write(f"{len(jobs_df)} sample job descriptions across software, data, cloud and AI roles.")
    st.dataframe(jobs_df[["job_id", "title", "company", "location", "experience_years"]], use_container_width=True, hide_index=True)
