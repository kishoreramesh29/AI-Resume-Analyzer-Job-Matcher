# AI Resume Analyzer & Job Matcher

An AI-powered web application that analyzes resumes, extracts important candidate information and skills, and matches candidates with relevant job opportunities.

Built with Python, NLP techniques, Scikit-learn, Pandas, and Streamlit.

---

## 📌 Project Overview

The **AI Resume Analyzer & Job Matcher** helps analyze a candidate's resume and identify relevant job opportunities based on skills and textual similarity.

The application performs resume parsing, text preprocessing, skill extraction, candidate analysis, and job matching.

Users can upload a resume and receive:

- Resume analysis
- Extracted skills
- Contact information
- Education information
- Experience information
- Certification information
- Job recommendations
- Job relevance scores
- Skill matching information
- Extracted resume text

---

## ✨ Features

### 📄 Resume Analysis

- Upload a resume through the Streamlit web interface
- Extract text from the uploaded resume
- Identify candidate information
- Extract technical and professional skills
- Detect education details
- Detect experience information
- Identify certifications

### 🔍 Skill Extraction

The system processes resume text and identifies skills from the available skills dataset.

Example skills include:

- Python
- SQL
- Machine Learning
- Data Analysis
- Pandas
- NumPy
- Scikit-learn
- NLP
- TensorFlow
- Java
- JavaScript

### 💼 Job Matching

The application compares resume content with job descriptions and calculates relevance scores.

The matching process considers:

- Resume text
- Job description
- Candidate skills
- Job-related skills
- Text similarity

### 📊 Job Ranking

Jobs are ranked according to their calculated relevance to the uploaded resume.

### 🌐 Interactive Web Application

The application uses Streamlit to provide an easy-to-use interface for resume analysis and job matching.

---

## 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| NLP | Resume text processing and analysis |
| Scikit-learn | TF-IDF and similarity calculations |
| Pandas | Dataset and data processing |
| NumPy | Numerical operations |
| Streamlit | Web application interface |
| PyPDF2 | PDF resume text extraction |

---

## 🔄 How It Works

```text
Resume Upload
      ↓
Resume Text Extraction
      ↓
Text Preprocessing
      ↓
Resume Information Analysis
      ↓
Skill Extraction
      ↓
Resume ↔ Job Description Matching
      ↓
Relevance Score Calculation
      ↓
Job Ranking
      ↓
Recommended Jobs