from pptx import Presentation
import os
from .text_cleaner import clean_text

def extract_text_from_ppt(filepath):
    """
    Extracts text from a PPTX file using python-pptx.
    Returns:
        dict: containing 'text', 'pages' (slides), and 'word_count'
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    prs = Presentation(filepath)
    full_text = []
    num_slides = len(prs.slides)
    
    for slide in prs.slides:
        slide_text = []
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text.append(shape.text)
        if slide_text:
            full_text.append("\n".join(slide_text))
            
    raw_text = "\n\n".join(full_text)
    cleaned_text = clean_text(raw_text)
    word_count = len(cleaned_text.split())
    
    return {
        "text": cleaned_text,
        "pages": num_slides,
        "word_count": word_count
    }
