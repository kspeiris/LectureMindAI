"""
Upgraded keyword extractor using KeyBERT with MMR diversity
and returning scored (keyword, score) tuples.
"""
from keybert import KeyBERT

_kw_model = None


def get_kw_model():
    global _kw_model
    if _kw_model is None:
        _kw_model = KeyBERT()   # uses all-MiniLM-L6-v2 by default
    return _kw_model


def extract_keywords(text: str, top_n: int = 15) -> str:
    """
    Extracts top N keywords/keyphrases using MMR for diversity.
    Returns a comma-separated string for DB storage.
    """
    if not text:
        return ""
    model = get_kw_model()
    results = model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        use_mmr=True,           # Maximal Marginal Relevance for diverse coverage
        diversity=0.5,
        top_n=top_n,
    )
    return ", ".join(kw for kw, _ in results)


def extract_keywords_scored(text: str, top_n: int = 15) -> list:
    """
    Returns a list of (keyword, score) tuples sorted by relevance score desc.
    Used by UI layers to render confidence-shaded pills.
    """
    if not text:
        return []
    model = get_kw_model()
    results = model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        use_mmr=True,
        diversity=0.5,
        top_n=top_n,
    )
    return sorted(results, key=lambda x: x[1], reverse=True)
