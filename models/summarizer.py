"""
Upgraded summarizer using flan-t5-base with instruction-tuned prompting.
Produces cleaner, bullet-point structured summaries.
"""
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import nltk
import re

MODEL_NAME = "google/flan-t5-base"

_tokenizer = None
_model = None


def get_summarizer():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return _tokenizer, _model


def sentence_aware_chunks(text: str, max_words: int = 350) -> list:
    """
    Splits text into chunks at sentence boundaries.
    Prevents cutting sentences mid-way which causes hallucinations.
    """
    try:
        sentences = nltk.sent_tokenize(text)
    except LookupError:
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
        sentences = nltk.sent_tokenize(text)

    chunks, current, count = [], [], 0
    for sent in sentences:
        wc = len(sent.split())
        if count + wc > max_words and current:
            chunks.append(" ".join(current))
            current, count = [sent], wc
        else:
            current.append(sent)
            count += wc
    if current:
        chunks.append(" ".join(current))
    return chunks


def _summarise_chunk(chunk: str, tokenizer, model) -> str:
    """Summarise a single chunk with an instruction-tuned prompt."""
    prompt = (
        "Summarize the following lecture content into clear, concise bullet points. "
        "Each bullet point should capture one key idea. Use '• ' to start each point.\n\n"
        f"Lecture content: {chunk}\n\n"
        "Summary:"
    )
    chunk_wc = len(chunk.split())
    max_l = min(180, max(50, int(chunk_wc * 0.45)))
    min_l = min(50, max(20, int(chunk_wc * 0.15)))

    try:
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
            padding=False,
        )
        ids = model.generate(
            inputs["input_ids"],
            max_length=max_l,
            min_length=min_l,
            num_beams=4,
            length_penalty=1.8,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )
        return tokenizer.decode(ids[0], skip_special_tokens=True).strip()
    except Exception as e:
        print(f"[Summarizer] Chunk error: {e}")
        return chunk[:300] + "..."


def _format_summary(raw: str) -> str:
    """
    Post-process model output:
    - Lines that don't start with '•' are wrapped as prose.
    - Lines that start with '-' are converted to '• '.
    - Consecutive bullet lines are preserved.
    """
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    formatted = []
    for line in lines:
        if line.startswith("•"):
            formatted.append(line)
        elif line.startswith("-"):
            formatted.append("• " + line.lstrip("- "))
        else:
            # Try splitting on ". " to extract implicit bullet points
            parts = re.split(r"\.\s+", line)
            if len(parts) > 1:
                for p in parts:
                    p = p.strip().rstrip(".")
                    if p:
                        formatted.append("• " + p + ".")
            else:
                formatted.append(line)
    return "\n".join(formatted)


def generate_summary(text: str) -> str:
    """
    Generates a high-quality structured summary using flan-t5-base.
    Returns bullet-formatted text ready for display.
    """
    if not text or len(text.split()) < 50:
        return text

    text = re.sub(r"\s+", " ", text).strip()
    tokenizer, model = get_summarizer()
    chunks = sentence_aware_chunks(text, max_words=350)

    raw_parts = [_summarise_chunk(c, tokenizer, model) for c in chunks]
    combined = "\n".join(raw_parts)
    return _format_summary(combined)
