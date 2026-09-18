import re
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def tokenize(text: str):
    text = normalize_text(text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    return [t for t in tokens if t not in ENGLISH_STOP_WORDS and len(t) > 1]

def clean_for_matching(text: str) -> str:
    tokens = tokenize(text)
    return " ".join(tokens)

def split_sentences(text: str):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
