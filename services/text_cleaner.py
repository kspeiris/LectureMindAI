import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Advanced cleaning for PDF/PPTX extracted text.
    Removes common extraction artifacts, fixes hyphenation, normalises unicode.
    """
    if not text:
        return ""

    # --- Unicode normalisation ---
    text = unicodedata.normalize("NFKC", text)

    # --- Curly/smart quotes → straight quotes ---
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')

    # --- Fix soft hyphen & hyphenated line-breaks ---
    text = text.replace("\u00ad", "")          # soft hyphen
    text = re.sub(r"-\s*\n\s*", "", text)      # "word-\nbreak" → "wordbreak"

    # --- Remove common PDF/PPTX noise ---
    # Bullet / list symbols
    text = re.sub(r"[•▪►▸➢●◉‣·]\s*", " ", text)
    # Slide / page number lines (standalone numbers or "Page N", "Slide N")
    text = re.sub(r"(?i)^\s*(slide|page)\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    # Running headers/footers: short lines (< 6 words) that repeat — remove standalone short lines
    lines = text.split("\n")
    filtered = []
    for line in lines:
        words = line.split()
        # Keep empty lines to preserve paragraph structure
        if len(words) == 0 or len(words) > 4:
            filtered.append(line)
        else:
            # Check if it looks like a title-cased header or just a number label
            joined = " ".join(words)
            if re.match(r"^[\d\W]+$", joined):
                continue   # pure symbols/numbers → skip
            filtered.append(line)
    text = "\n".join(filtered)

    # --- Whitespace normalisation ---
    text = re.sub(r"\n{3,}", "\n\n", text)    # max 2 consecutive newlines
    text = re.sub(r" {2,}", " ", text)         # collapse multiple spaces
    text = text.replace("\xa0", " ")            # non-breaking space
    text = text.replace("\t", " ")              # tabs → space

    # --- Strip ---
    text = text.strip()

    return text
