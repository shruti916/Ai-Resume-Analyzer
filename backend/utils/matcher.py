from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from spacy.lang.en.stop_words import STOP_WORDS

# Add custom stopwords for job-ad fluff
CUSTOM_STOPWORDS = {
    # generic hiring words
    "looking", "seeking", "wanted", "hiring", "join",
    "opportunity", "career", "position", "candidate", "applicant", "det",

    # fluffy adjectives
    "professional", "ideal", "dynamic", "exciting", "motivated",
    "passionate", "driven", "talented", "skilled", "strong",
    "excellent", "good", "great", "successful", "valuable", "produktiv",

    # vague nouns
    "experience", "knowledge", "ability", "expectations",
    "solutions", "quality", "building", "specific", "background",
    "expertise", "impact", "environment", "culture", "team", "plus","lookout",

    # filler verbs
    "work", "working", "collaborate", "provide", "deliver",
    "create", "build", "develop", "support", "ensure",

    # business buzzwords
    "innovative", "scalable", "seamless", "future", "global",
    "leader", "market", "business", "success", "growth"
}

def clean_text(text: str) -> str:
    """Basic text cleanup: lowercase, remove non-letters."""
    return re.sub(r'[^a-zA-Z\s]', ' ', text).lower()

def compute_similarity(resume_text: str, job_text: str):
    """Return hybrid similarity score + missing keywords."""
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    # Vectorize with built-in stopwords
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([resume_text, job_text])
    cosine_score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    # Token sets
    job_words = set(job_text.split())
    resume_words = set(resume_text.split())

    # Filter missing keywords
    missing = [
        w for w in (job_words - resume_words)
        if w not in STOP_WORDS and w not in CUSTOM_STOPWORDS and len(w) > 2
    ]

    # Keyword overlap score
    overlap_score = len(job_words & resume_words) / len(job_words) if job_words else 0

    # Hybrid score (60% cosine + 40% overlap)
    final_score = (0.6 * cosine_score + 0.4 * overlap_score) * 100

    return {
        "score": round(final_score, 2),
        "missing_keywords": missing[:15]
    }
