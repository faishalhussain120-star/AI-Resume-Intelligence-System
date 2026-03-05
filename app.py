import streamlit as st
import pandas as pd

from utils import extract_text_from_pdf, calculate_similarity
from skills import extract_skills, skill_score

st.set_page_config(
    page_title="AI Resume Intelligence System",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Resume Intelligence System")

st.sidebar.header("⚙️ Scoring Weights")

similarity_weight = st.sidebar.slider("Similarity Weight", 0.0, 1.0, 0.5)
skill_weight = st.sidebar.slider("Skill Weight", 0.0, 1.0, 0.5)

col1, col2 = st.columns(2)

with col1:
    job_desc = st.text_area("📄 Paste Job Description")

with col2:
    uploaded_resumes = st.file_uploader(
        "📂 Upload Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

if st.button("🔍 Analyze Candidates"):

    if job_desc and uploaded_resumes:

        with st.spinner("Analyzing resumes..."):

            resume_texts = []
            resume_names = []

            for resume in uploaded_resumes:
                text = extract_text_from_pdf(resume)
                resume_texts.append(text)
                resume_names.append(resume.name)

            similarity_scores = calculate_similarity(job_desc, resume_texts)

            job_skills = extract_skills(job_desc)

            results_data = []

            for i in range(len(resume_texts)):

                resume_skills = extract_skills(resume_texts[i])

                sim_score = similarity_scores[i] * 100
                sk_score = skill_score(job_skills, resume_skills)

                final_score = (
                    similarity_weight * sim_score +
                    skill_weight * sk_score
                )

                results_data.append([
                    resume_names[i],
                    round(sim_score,2),
                    round(sk_score,2),
                    round(final_score,2)
                ])

            results = pd.DataFrame(
                results_data,
                columns=[
                    "Candidate",
                    "Semantic Similarity %",
                    "Skill Match %",
                    "Final Score %"
                ]
            )

            results = results.sort_values(
                by="Final Score %",
                ascending=False
            )

            st.success("✅ Analysis Complete")

            st.metric(
                "🏆 Top Candidate",
                results.iloc[0]["Candidate"]
            )

            st.dataframe(results)

            st.bar_chart(
                results.set_index("Candidate")["Final Score %"]
            )

            csv = results.to_csv(index=False)

            st.download_button(
                "⬇ Download Results",
                csv,
                "resume_ranking.csv",
                "text/csv"
            )

    else:
        st.warning("Please provide job description and upload resumes.")