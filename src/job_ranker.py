import pandas as pd
from .skill_extractor import extract_skills, estimate_experience_years
from .matcher import calculate_match

def rank_jobs(resume_text, jobs_df, skills_df):
    resume_skills = extract_skills(resume_text, skills_df)
    resume_years = estimate_experience_years(resume_text)

    results = []
    for _, row in jobs_df.iterrows():
        job_text = f"{row['title']} {row['description']} {row['requirements']}"
        job_skills = extract_skills(job_text, skills_df)
        required_years = float(row.get("experience_years", 0) or 0)

        metrics = calculate_match(
            resume_text, job_text, resume_skills, job_skills,
            resume_years, required_years
        )

        matching = sorted(
            set(map(str.lower, resume_skills)) & set(map(str.lower, job_skills))
        )
        missing = sorted(
            set(map(str.lower, job_skills)) - set(map(str.lower, resume_skills))
        )

        # Restore readable capitalization from the skills dataset.
        display = {s.lower(): s for s in skills_df["skill"]}
        matching = [display.get(s, s) for s in matching]
        missing = [display.get(s, s) for s in missing]

        results.append({
            "job_id": row["job_id"],
            "title": row["title"],
            "company": row["company"],
            "location": row["location"],
            "description": row["description"],
            "requirements": row["requirements"],
            "score": metrics["score"],
            "similarity": metrics["similarity"],
            "skill_coverage": metrics["skill_coverage"],
            "experience_alignment": metrics["experience_alignment"],
            "matching_skills": matching,
            "missing_skills": missing,
        })

    return pd.DataFrame(results).sort_values("score", ascending=False).reset_index(drop=True)
