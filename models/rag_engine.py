from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

# Directory to save indices
INDEX_DIR = os.path.join(os.path.dirname(__file__), '..', 'vectorstore', 'faiss_index')
META_DIR = os.path.join(os.path.dirname(__file__), '..', 'vectorstore', 'metadata')

os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

MODEL_NAME = 'all-MiniLM-L6-v2'
_embed_model = None

def get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(MODEL_NAME)
    return _embed_model

def get_index_path(lecture_id):
    return os.path.join(INDEX_DIR, f"lecture_{lecture_id}.index")

def get_meta_path(lecture_id):
    return os.path.join(META_DIR, f"lecture_{lecture_id}.pkl")

def chunk_text_for_rag(text, chunk_size=500, overlap=50):
    """Simple word-based chunking with overlap."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def build_faiss_index(lecture_id, text):
    """
    Chunks the text, embeds it, and builds a FAISS index.
    Saves the index and the chunk metadata (text) to disk.
    """
    if not text:
        return
        
    chunks = chunk_text_for_rag(text)
    model = get_embed_model()
    embeddings = model.encode(chunks, convert_to_numpy=True)
    
    # Initialize FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Save index
    faiss.write_index(index, get_index_path(lecture_id))
    
    # Save metadata (the actual text chunks)
    with open(get_meta_path(lecture_id), 'wb') as f:
        pickle.dump(chunks, f)

def query_rag(lecture_id, query, top_k=3):
    """
    Retrieves the top-k chunks relevant to the query from the FAISS index.
    In a full RAG, this would be passed to a generation model.
    Here we return the context directly as the "answer" or pass it to a lightweight generator.
    """
    index_path = get_index_path(lecture_id)
    meta_path = get_meta_path(lecture_id)
    
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        return "Knowledge base not found for this lecture. Please re-upload or process it."
        
    index = faiss.read_index(index_path)
    with open(meta_path, 'rb') as f:
        chunks = pickle.load(f)
        
    model = get_embed_model()
    query_vector = model.encode([query], convert_to_numpy=True)
    
    distances, indices = index.search(query_vector, top_k)
    
    retrieved_contexts = []
    for idx in indices[0]:
        if idx < len(chunks):
            retrieved_contexts.append(chunks[idx])
            
    context = "\n\n---\n\n".join(retrieved_contexts)
    
    # Since we don't want to load a huge LLM just for chat, we will construct a prompt-like response
    # Or we can just return the extracted contexts as citations.
    
    response = "Based on the lecture materials:\n\n"
    for i, ctx in enumerate(retrieved_contexts):
        response += f"**Excerpt {i+1}:** {ctx}\n\n"
        
    return response

