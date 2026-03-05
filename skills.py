SKILLS = [
    "python","machine learning","deep learning",
    "nlp","data analysis","pandas","numpy",
    "scikit-learn","sql","tensorflow","keras",
    "git","github","streamlit","flask","django"
]

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return list(set(found))

def skill_score(job_skills, resume_skills):
    if len(job_skills) == 0:
        return 0
    matched = set(job_skills).intersection(set(resume_skills))
    return (len(matched)/len(job_skills))*100