# AI-Powered Resume Analyzer & Job Matcher

A complete Python/NLP/ML portfolio project that:
- extracts text from PDF, DOCX and TXT resumes
- extracts skills, education, experience and certifications
- compares a resume against job descriptions
- calculates TF-IDF/cosine-similarity match scores
- identifies matching and missing skills
- ranks multiple jobs
- generates actionable recommendations
- provides a Streamlit web interface

## 1. Installation

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2. Run

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## 3. Project structure

```text
resume_job_matcher/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── jobs.csv
│   └── skills.csv
├── src/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── text_processor.py
│   ├── skill_extractor.py
│   ├── matcher.py
│   ├── job_ranker.py
│   └── analyzer.py
├── tests/
│   └── test_matcher.py
└── uploads/
```

## 4. Dataset

`data/jobs.csv` contains synthetic job descriptions for demonstration and testing.
`data/skills.csv` contains the skill dictionary used by the rule-based skill extractor.

For a production system, replace the synthetic dataset with licensed/real job data and expand the skill taxonomy.

## 5. Matching approach

The default score combines:
- 60% TF-IDF cosine similarity between resume and job description
- 30% skill coverage
- 10% experience/education keyword alignment

This is intentionally interpretable and easy to explain in an interview.

## 6. Optional upgrade

You can later add Sentence Transformers for embedding-based semantic matching. The current version does not require a large pretrained model download, so it runs easily on a normal laptop.

## 7. Testing

```bash
python -m unittest discover -s tests -v
```
