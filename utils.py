import PyPDF2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

def extract_text_from_pdf(uploaded_file):
    try:
        text = ""
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text
    except Exception as e:
        return ""

def calculate_similarity(job_desc, resumes):
    job_embedding = model.encode([job_desc])
    resume_embeddings = model.encode(resumes)
    scores = cosine_similarity(job_embedding, resume_embeddings)
    return scores[0]