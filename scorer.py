import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the NLP language model
nlp = spacy.load("en_core_web_sm")

def analyze_resume_vs_jd(resume_text: str, job_description: str) -> dict:
    """Scores a resume against a job description using TF-IDF Vectorization and NLP."""
    # 1. Clean and normalize texts to lowercase
    clean_resume = resume_text.lower()
    clean_jd = job_description.lower()

    # 2. Compute Match Percentage using TF-IDF & Cosine Similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_jd])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    ats_score = round(float(similarity[0][0]) * 100, 1)

    # 3. NLP Tokenization & Skill Keyword Extraction
    jd_doc = nlp(clean_jd)
    resume_doc = nlp(clean_resume)

    # Extract standard nouns and proper nouns as keyword/skill targets
    jd_keywords = {token.text for token in jd_doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop}
    resume_keywords = {token.text for token in resume_doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop}

    # Find what keywords are missing from the resume
    missing_keywords = list(jd_keywords - resume_keywords)[:8]  # Limit to top 8 actionable insights

    # 4. Generate Formatting Feedback Warnings
    warnings = []
    if len(resume_text) > 6000:
        warnings.append("Resume length is text-heavy (Over 2 pages equivalent). Consider condensing.")
    if "table" in clean_resume or "box" in clean_resume:
        warnings.append("Potential complex layout detected. Stick to simple text columns.")

    return {
        "ats_score": ats_score if ats_score > 0 else 15.0,  # Fallback baseline floor score
        "missing_keywords": missing_keywords,
        "warnings": warnings if warnings else ["No major formatting issues detected! Perfect formatting structure."]
    }