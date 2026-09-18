from pathlib import Path
import pandas as pd
import re

def load_skills(path="data/skills.csv"):
    df = pd.read_csv(path)
    df["skill"] = df["skill"].astype(str)
    df["normalized"] = df["skill"].str.lower().str.strip()
    return df

def _skill_pattern(skill: str):
    # Match phrases without requiring word boundaries inside the phrase.
    escaped = re.escape(skill.lower())
    return re.compile(r"(?<!\w)" + escaped + r"(?!\w)", re.I)

def extract_skills(text: str, skills_df=None):
    if skills_df is None:
        skills_df = load_skills()
    found = []
    lower = text.lower()
    for skill in skills_df["skill"].tolist():
        if _skill_pattern(skill).search(lower):
            found.append(skill)
    # Remove duplicates while preserving dataset order.
    return list(dict.fromkeys(found))

def extract_section(text: str, headings):
    lines = [line.strip() for line in text.splitlines()]
    headings_lower = {h.lower() for h in headings}
    captured = []
    active = False
    for line in lines:
        normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
        if normalized in headings_lower:
            active = True
            continue
        if active and re.match(r"^[A-Z][A-Za-z &/]{2,40}:?$", line) and line.lower().rstrip(":") in headings_lower:
            break
        if active:
            captured.append(line)
    return "\n".join(captured).strip()

def extract_education(text: str):
    patterns = [
        r"\b(?:B\.?E\.?|B\.?Tech|Bachelor(?:'s)?|M\.?E\.?|M\.?Tech|Master(?:'s)?|B\.?Sc|M\.?Sc|MBA|MCA|Ph\.?D\.?)\b[^.\n]{0,100}",
        r"\b(?:Computer Science|Information Technology|Data Science|Electronics|Mechanical|Business Administration)\b",
    ]
    results = []
    for p in patterns:
        results.extend(re.findall(p, text, flags=re.I))
    return list(dict.fromkeys([x.strip(" -,:") for x in results]))[:10]

def estimate_experience_years(text: str):
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", text, flags=re.I)
    if not matches:
        return 0.0
    return max(float(x) for x in matches)

def extract_certifications(text: str):
    patterns = [
        r"(?:AWS Certified[^.\n]*|Microsoft Certified[^.\n]*|Google Cloud[^.\n]*|TensorFlow Developer[^.\n]*|Oracle Certified[^.\n]*)"
    ]
    out = []
    for p in patterns:
        out.extend(re.findall(p, text, flags=re.I))
    return list(dict.fromkeys([x.strip() for x in out]))[:10]
