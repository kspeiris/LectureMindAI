import pdfplumber
import os
from .text_cleaner import clean_text


def extract_text_from_pdf(filepath: str) -> dict:
    """
    Extracts and cleans text from a PDF using pdfplumber.
    Skips table regions to avoid noisy structured data blurring the prose.

    Returns:
        dict: {'text': str, 'pages': int, 'word_count': int}
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    page_texts = []
    num_pages = 0

    with pdfplumber.open(filepath) as pdf:
        num_pages = len(pdf.pages)
        for page in pdf.pages:
            # Get bounding boxes of tables so we can exclude them
            table_bboxes = [tbl.bbox for tbl in page.find_tables()]

            if table_bboxes:
                # Filter out words that fall inside any table bbox
                words = page.extract_words()
                prose_words = []
                for w in words:
                    wx0, wy0, wx1, wy1 = w["x0"], w["top"], w["x1"], w["bottom"]
                    in_table = any(
                        tx0 <= wx0 and wy0 >= ty0 and wx1 <= tx1 and wy1 <= ty1
                        for tx0, ty0, tx1, ty1 in table_bboxes
                    )
                    if not in_table:
                        prose_words.append(w["text"])
                extracted = " ".join(prose_words)
            else:
                extracted = page.extract_text() or ""

            cleaned = clean_text(extracted)
            if cleaned:
                page_texts.append(cleaned)

    full_text = "\n\n".join(page_texts)
    full_text = clean_text(full_text)   # second-pass global clean
    word_count = len(full_text.split())

    return {
        "text": full_text,
        "pages": num_pages,
        "word_count": word_count,
    }
