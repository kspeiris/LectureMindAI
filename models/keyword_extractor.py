from keybert import KeyBERT

_kw_model = None

def get_kw_model():
    global _kw_model
    if _kw_model is None:
        # Uses sentence-transformers/all-MiniLM-L6-v2 by default
        _kw_model = KeyBERT()
    return _kw_model

def extract_keywords(text, top_n=10):
    """
    Extracts top N keywords/keyphrases from the text.
    Returns a comma-separated string of keywords.
    """
    if not text:
        return ""
        
    model = get_kw_model()
    # Extract keywords
    keywords_with_scores = model.extract_keywords(
        text, 
        keyphrase_ngram_range=(1, 2), 
        stop_words='english', 
        use_maxsum=True, 
        nr_candidates=20, 
        top_n=top_n
    )
    
    # Just return the words
    keywords = [kw[0] for kw in keywords_with_scores]
    return ", ".join(keywords)
