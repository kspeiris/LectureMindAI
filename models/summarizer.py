from transformers import pipeline
import textwrap

# Using a smaller BART model for better local performance
# You can switch to "facebook/bart-large-cnn" if you have a powerful GPU
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

# Load the summarization pipeline lazily
_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model=MODEL_NAME)
    return _summarizer

def chunk_text(text, max_chunk_len=3000):
    """Splits text into chunks of maximum length to fit in model context window."""
    return textwrap.wrap(text, max_chunk_len, break_long_words=False, replace_whitespace=False)

def generate_summary(text):
    """
    Generates a summary for the given text. Handles long texts by chunking.
    """
    if not text or len(text.split()) < 50:
        return text # Too short to summarize
        
    summarizer = get_summarizer()
    chunks = chunk_text(text)
    
    summaries = []
    for chunk in chunks:
        # max_length constraints based on the length of the chunk
        chunk_len = len(chunk.split())
        max_l = min(130, max(30, int(chunk_len * 0.5)))
        min_l = min(30, max(10, int(chunk_len * 0.2)))
        
        try:
            res = summarizer(chunk, max_length=max_l, min_length=min_l, do_sample=False)
            summaries.append(res[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing chunk: {e}")
            summaries.append(chunk[:200] + "...") # Fallback
            
    final_summary = " ".join(summaries)
    return final_summary
