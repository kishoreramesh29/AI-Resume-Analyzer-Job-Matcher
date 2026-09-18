from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .text_processor import clean_for_matching

def tfidf_similarity(resume_text: str, job_text: str) -> float:
    docs = [clean_for_matching(resume_text), clean_for_matching(job_text)]
    if not any(docs):
        return 0.0
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    matrix = vectorizer.fit_transform(docs)
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])

def skill_coverage(resume_skills, job_skills):
    r = {s.lower() for s in resume_skills}
    j = {s.lower() for s in job_skills}
    if not j:
        return 0.0
    return len(r & j) / len(j)

def experience_score(resume_years, required_years):
    if required_years <= 0:
        return 1.0
    return min(resume_years / required_years, 1.0)

def calculate_match(resume_text, job_text, resume_skills, job_skills,
                    resume_years=0.0, required_years=0.0):
    sim = tfidf_similarity(resume_text, job_text)
    coverage = skill_coverage(resume_skills, job_skills)
    exp = experience_score(resume_years, required_years)

    score = (0.60 * sim) + (0.30 * coverage) + (0.10 * exp)
    return {
        "similarity": sim,
        "skill_coverage": coverage,
        "experience_alignment": exp,
        "score": score,
    }
