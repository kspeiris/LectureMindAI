import pdfplumber
import os
from .text_cleaner import clean_text

def extract_text_from_pdf(filepath):
    """
    Extracts text from a PDF file using pdfplumber.
    Returns:
        dict: containing 'text', 'pages', and 'word_count'
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    full_text = []
    num_pages = 0
    
    with pdfplumber.open(filepath) as pdf:
        num_pages = len(pdf.pages)
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                full_text.append(extracted)
                
    raw_text = "\n".join(full_text)
    cleaned_text = clean_text(raw_text)
    word_count = len(cleaned_text.split())
    
    return {
        "text": cleaned_text,
        "pages": num_pages,
        "word_count": word_count
    }
