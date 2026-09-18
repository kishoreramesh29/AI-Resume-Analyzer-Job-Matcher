from .skill_extractor import extract_skills, extract_education, extract_certifications, estimate_experience_years

def analyze_resume(text, skills_df):
    skills = extract_skills(text, skills_df)
    education = extract_education(text)
    certifications = extract_certifications(text)
    experience = estimate_experience_years(text)

    recommendations = []
    if not skills:
        recommendations.append("Add a clear Skills section with technical and professional skills.")
    if not education:
        recommendations.append("Add your degree, institution, and graduation year.")
    if experience == 0:
        recommendations.append("Use measurable experience statements such as '2+ years' where applicable.")
    if len(skills) < 5:
        recommendations.append("Consider adding more relevant tools, frameworks, databases, or cloud technologies you genuinely know.")

    return {
        "skills": skills,
        "education": education,
        "certifications": certifications,
        "experience_years": experience,
        "recommendations": recommendations,
    }
