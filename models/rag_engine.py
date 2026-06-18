"""
Upgraded RAG engine using flan-t5-base with richer prompts,
higher top_k retrieval, and confidence scoring.
"""
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import faiss
import numpy as np
import os
import pickle
import nltk

INDEX_DIR = os.path.join(os.path.dirname(__file__), '..', 'vectorstore', 'faiss_index')
META_DIR  = os.path.join(os.path.dirname(__file__), '..', 'vectorstore', 'metadata')

os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

EMBED_MODEL = 'all-MiniLM-L6-v2'
GEN_MODEL   = 'google/flan-t5-base'   # upgraded from flan-t5-small

_embed_model    = None
_gen_tokenizer  = None
_gen_model      = None


def get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBED_MODEL)
    return _embed_model


def get_gen_model():
    global _gen_tokenizer, _gen_model
    if _gen_model is None:
        _gen_tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
        _gen_model     = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL)
    return _gen_tokenizer, _gen_model


def get_index_path(lecture_id):
    return os.path.join(INDEX_DIR, f"lecture_{lecture_id}.index")


def get_meta_path(lecture_id):
    return os.path.join(META_DIR, f"lecture_{lecture_id}.pkl")


# ─────────────────────────────────────────────────────────────
# Text chunking
# ─────────────────────────────────────────────────────────────

def semantic_chunk_text(text: str, max_words: int = 150, overlap_sentences: int = 2) -> list:
    """
    Chunk text at sentence boundaries with configurable overlap for
    richer context retrieval. Overlap=2 ensures no fact is split
    across a chunk boundary without context.
    """
    try:
        sentences = nltk.sent_tokenize(text)
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        sentences = nltk.sent_tokenize(text)

    chunks, current, count = [], [], 0
    for sent in sentences:
        wc = len(sent.split())
        if count + wc > max_words and current:
            chunks.append(" ".join(current))
            current = current[-overlap_sentences:]
            count   = sum(len(s.split()) for s in current)
        current.append(sent)
        count += wc
    if current:
        chunks.append(" ".join(current))
    return chunks


# ─────────────────────────────────────────────────────────────
# Index building
# ─────────────────────────────────────────────────────────────

def build_faiss_index(lecture_id: int, text: str):
    """
    Chunks the text semantically, embeds each chunk, and builds a
    FAISS cosine-similarity index.
    """
    if not text:
        return

    chunks    = semantic_chunk_text(text)
    model     = get_embed_model()
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=False)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)   # inner-product = cosine after L2-norm
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    faiss.write_index(index, get_index_path(lecture_id))
    with open(get_meta_path(lecture_id), 'wb') as f:
        pickle.dump(chunks, f)


# ─────────────────────────────────────────────────────────────
# RAG query
# ─────────────────────────────────────────────────────────────

def query_rag(lecture_id: int, query: str, top_k: int = 5) -> str:
    """
    True RAG pipeline:
      1. Embed the query
      2. Retrieve top_k most relevant chunks (cosine similarity)
      3. Synthesise a natural-language answer with flan-t5-base
      4. Return answer + source excerpts + confidence score
    """
    index_path = get_index_path(lecture_id)
    meta_path  = get_meta_path(lecture_id)

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        return (
            "⚠️ **Knowledge base not found** for this lecture. "
            "Please go to **Notes Generator** and process this lecture first."
        )

    index = faiss.read_index(index_path)
    with open(meta_path, 'rb') as f:
        chunks = pickle.load(f)

    embed_model  = get_embed_model()
    query_vector = embed_model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_vector)

    k = min(top_k, len(chunks))
    distances, indices = index.search(query_vector, k)

    retrieved   = []
    conf_scores = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(chunks):
            retrieved.append(chunks[idx])
            conf_scores.append(float(dist))   # cosine similarity in [0, 1] after normalisation

    if not retrieved:
        return "I couldn't find relevant information in the lecture for your question."

    # Build context from top chunks
    context = " ".join(retrieved)[:1500]
    top_confidence = conf_scores[0] if conf_scores else 0.0

    # ── flan-t5-base answer synthesis ──────────────────────────────────────
    try:
        tokenizer, model = get_gen_model()
        # Put question first so it never gets truncated if context is too long
        prompt = (
            "You are a comprehensive AI Study Assistant. Answer the question fully and completely in detail using ONLY the provided lecture context. "
            f"Question: {query}\n\n"
            f"Context: {context}\n\n"
            "Answer:"
        )
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(
            inputs["input_ids"],
            max_new_tokens=300,
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=3,
            length_penalty=2.0,
        )
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    except Exception as e:
        answer = "I found relevant content but had trouble generating an answer. Please try rephrasing."

    # ── Confidence label ────────────────────────────────────────────────────
    if top_confidence >= 0.75:
        conf_label = "🟢 High"
    elif top_confidence >= 0.50:
        conf_label = "🟡 Medium"
    else:
        conf_label = "🔴 Low"

    # ── Final response ──────────────────────────────────────────────────────
    response = (
        f"**📖 Answer:**\n\n{answer}\n\n"
        f"<span class='inline-block bg-emerald-400/10 border border-emerald-400/20 rounded-md px-2 py-0.5 text-xs text-emerald-400 font-semibold'>Relevance: {conf_label} ({top_confidence:.0%})</span>\n\n"
        "---\n\n**📚 Sources from Lecture:**\n"
    )
    for i, (ctx, score) in enumerate(zip(retrieved[:3], conf_scores[:3])):
        excerpt = ctx[:280] + ("..." if len(ctx) > 280 else "")
        response += f"\n> **Excerpt {i+1}** *(similarity: {score:.0%})*: {excerpt}\n"

    return response
