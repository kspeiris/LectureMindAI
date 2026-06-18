import re

def clean_text(text):
    """
    Cleans extracted text by removing extra whitespaces, newlines,
    and handling common PDF/PPTX artifact issues.
    """
    if not text:
        return ""
        
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    
    # Remove unwanted invisible characters (like non-breaking spaces)
    text = text.replace('\xa0', ' ')
    
    # Strip leading/trailing whitespaces
    text = text.strip()
    
    return text
