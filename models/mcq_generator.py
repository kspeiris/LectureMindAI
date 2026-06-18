"""
Upgraded MCQ & Flashcard generator using flan-t5-base.
Key improvements:
  - Instruction-tuned prompts for cleaner questions
  - Model-generated distractors (not raw sentence dumps)
  - Distractor trimming to ≤ 15 words for concise options
  - Quality filter to skip malformed questions
"""
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import nltk
import random
import re

MODEL_NAME = "google/flan-t5-base"

_tokenizer = None
_model = None


def get_generator():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return _tokenizer, _model


# ─────────────────────────────────────────────
# Sentence utilities
# ─────────────────────────────────────────────

def get_sentences(text: str, max_sentences: int = 30) -> list:
    """Extract clean, meaningful sentences using NLTK."""
    try:
        sentences = nltk.sent_tokenize(text)
    except LookupError:
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
        sentences = nltk.sent_tokenize(text)

    sentences = [
        s.strip() for s in sentences
        if 8 < len(s.split()) < 70
        and not re.match(r"^\s*[\d\W]+\s*$", s)   # skip pure number/symbol lines
    ]
    if len(sentences) > max_sentences:
        # Spread sample across full document for diversity
        step = max(1, len(sentences) // max_sentences)
        sentences = sentences[::step][:max_sentences]
    return sentences


def _trim_to_words(text: str, max_words: int = 15) -> str:
    """Trim a string to at most max_words words."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(",.;:") + "..."


def _is_valid_question(q: str) -> bool:
    """Return True if a generated question looks plausible."""
    if not q or len(q.split()) < 4:
        return False
    # Should end with '?' after normalisation
    # Should contain at least one verb-like word
    if len(q) > 250:
        return False
    return True


# ─────────────────────────────────────────────
# Question generation
# ─────────────────────────────────────────────

def generate_question_from_sentence(sentence: str, tokenizer, model) -> str | None:
    """Use flan-t5-base to generate a focused study question from a sentence."""
    prompt = (
        "Generate one clear, specific study question based on the key fact in this sentence. "
        "The question must end with a question mark.\n\n"
        f"Sentence: {sentence}\n\n"
        "Question:"
    )
    try:
        inputs = tokenizer(prompt, return_tensors="pt", max_length=384, truncation=True)
        outputs = model.generate(
            inputs["input_ids"],
            max_length=80,
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=2,
            length_penalty=1.2,
        )
        question = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        if question and not question.endswith("?"):
            question += "?"
        return question if _is_valid_question(question) else None
    except Exception:
        return None


# ─────────────────────────────────────────────
# Distractor generation
# ─────────────────────────────────────────────

def generate_distractors_with_model(
    question: str, correct_answer: str, tokenizer, model, n: int = 3
) -> list:
    """
    Use flan-t5-base to produce short, plausible-but-wrong distractor options.
    Falls back to keyword-shuffled alternatives if generation fails.
    """
    prompt = (
        f"Question: {question}\n"
        f"Correct answer: {_trim_to_words(correct_answer, 12)}\n\n"
        f"Generate {n} short, plausible but WRONG answer options (each ≤ 12 words, separated by '|').\n"
        "Wrong options:"
    )
    distractors = []
    try:
        inputs = tokenizer(prompt, return_tensors="pt", max_length=384, truncation=True)
        outputs = model.generate(
            inputs["input_ids"],
            max_length=120,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=2,
        )
        raw = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        # Parse pipe-separated or newline-separated output
        parts = re.split(r"[|\n]", raw)
        for part in parts:
            part = part.strip().strip("0123456789.)- \t")
            if part and part.lower() != correct_answer.lower()[:20].lower():
                distractors.append(_trim_to_words(part, 15))
    except Exception:
        pass

    # ── Fallback: generic academic distractors ──────────────────────────────
    generic_pool = [
        "It depends on external conditions not covered here.",
        "None of the above concepts apply.",
        "This process occurs during a different phase.",
        "The opposite mechanism is responsible.",
        "This factor has no measurable effect here.",
        "It is determined solely by environmental inputs.",
        "All of the above options are equally valid.",
        "This is a property of an unrelated system.",
    ]
    random.shuffle(generic_pool)
    for g in generic_pool:
        if len(distractors) >= n:
            break
        if g not in distractors:
            distractors.append(g)

    return distractors[:n]


# ─────────────────────────────────────────────
# Flashcard generation
# ─────────────────────────────────────────────

def generate_flashcards(text: str, num_cards: int = 8) -> list:
    """
    Generates Q&A flashcards using NLTK sentence extraction + flan-t5-base question generation.
    """
    if not text:
        return []

    tokenizer, model = get_generator()
    sentences = get_sentences(text, max_sentences=num_cards + 10)
    random.shuffle(sentences)

    flashcards = []
    for sentence in sentences:
        if len(flashcards) >= num_cards:
            break
        question = generate_question_from_sentence(sentence, tokenizer, model)
        if question:
            # Trim answer to a clean, concise sentence
            answer = _trim_to_words(sentence, 40)
            flashcards.append({"question": question, "answer": answer})

    # Fallback: cloze-style cards
    for sentence in sentences:
        if len(flashcards) >= num_cards:
            break
        words = sentence.split()
        if len(words) > 6:
            first = " ".join(words[:5])
            flashcards.append({
                "question": f"Complete this concept: '{first} …'",
                "answer": _trim_to_words(sentence, 40),
            })

    return flashcards[:num_cards]


# ─────────────────────────────────────────────
# MCQ generation
# ─────────────────────────────────────────────

def generate_mcqs(text: str, num_mcqs: int = 8) -> list:
    """
    Generates multiple-choice questions with model-generated concise distractors.
    Each option is a short phrase (≤ 15 words), not a raw paragraph.
    """
    if not text:
        return []

    tokenizer, model = get_generator()
    flashcards = generate_flashcards(text, num_cards=num_mcqs)

    mcqs = []
    for fc in flashcards:
        correct_trimmed = _trim_to_words(fc["answer"], 15)
        distractors = generate_distractors_with_model(
            fc["question"], correct_trimmed, tokenizer, model, n=3
        )

        options = distractors[:3] + [correct_trimmed]
        random.shuffle(options)

        # De-duplicate
        seen, unique = set(), []
        for opt in options:
            key = opt.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(opt)

        if correct_trimmed not in unique:
            unique.append(correct_trimmed)

        mcqs.append({
            "question": fc["question"],
            "options": unique[:4],
            "correct": correct_trimmed,
        })

    return mcqs
