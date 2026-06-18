import hashlib
import os

import streamlit as st

from database.database import add_lecture, check_duplicate_file
from services.pdf_processor import extract_text_from_pdf
from services.ppt_processor import extract_text_from_ppt
from utils.styles import inject_css, page_header

inject_css()
page_header("📤 Upload Lecture", "Upload a lecture file or paste raw text to begin.")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(os.path.join(UPLOAD_DIR, "pdfs"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "pptx"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "texts"), exist_ok=True)

tab_file, tab_text = st.tabs(["📄 Upload File", "📝 Paste Text"])

with tab_file:
    uploaded_file = st.file_uploader(
        "Choose a lecture file",
        type=["pdf", "pptx", "txt"],
        help="Supported formats: PDF, PowerPoint, and plain text files.",
    )

with tab_text:
    pasted_text = st.text_area(
        "Paste lecture text",
        height=220,
        placeholder="Paste notes, transcripts, or article text here...",
    )

has_file = uploaded_file is not None
has_text = bool(pasted_text.strip())

if not has_file and not has_text:
    st.info("Choose a file or paste lecture text to preview and process it.")
    st.stop()

if has_file and has_text:
    st.warning("Please use either file upload or pasted text, not both at the same time.")
    st.stop()

if has_file:
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name
    source_label = "Uploaded file"
else:
    file_bytes = pasted_text.encode("utf-8")
    filename = "pasted_text.txt"
    source_label = "Pasted text"

file_hash = hashlib.md5(file_bytes).hexdigest()
file_ext = filename.split(".")[-1].lower()
file_size_kb = len(file_bytes) / 1024

st.html(
    f"""
    <div class="info-strip">
        <strong>{filename if has_file else "Pasted Text"}</strong>
        &nbsp;·&nbsp; {file_size_kb:.1f} KB
        &nbsp;·&nbsp; {source_label}
    </div>
    """
)

existing = check_duplicate_file(file_hash)
if existing:
    st.warning(
        f"Duplicate detected. This content was already uploaded as "
        f"'{existing['title']}' on {existing['upload_date'][:10]}."
    )

suggested_title = (
    filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
    if has_file
    else "Pasted Notes"
)
custom_title = st.text_input(
    "Lecture title",
    value=suggested_title,
    placeholder="Give this lecture a meaningful name",
    help="This title appears in notes, flashcards, quizzes, and chat.",
)

if st.button("⚙️ Process Lecture"):
    if not custom_title.strip():
        st.error("Please enter a title for this lecture.")
        st.stop()

    if not has_file:
        filename = f"pasted_{file_hash[:8]}.txt"

    save_dir = "texts" if file_ext == "txt" else f"{file_ext}s"
    file_path = os.path.join(UPLOAD_DIR, save_dir, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    progress = st.progress(0)
    status = st.empty()

    def step(message: str, pct: int, state: str = "active"):
        status.html(
            f"<div class='step-item {state}'>⏳ {message}</div>"
        )
        progress.progress(pct)

    try:
        step("Extracting text from lecture content...", 20)
        if file_ext == "pdf":
            data = extract_text_from_pdf(file_path)
        elif file_ext == "pptx":
            data = extract_text_from_ppt(file_path)
        elif file_ext == "txt":
            text_content = file_bytes.decode("utf-8", errors="ignore")
            data = {
                "text": text_content,
                "pages": 1,
                "word_count": len(text_content.split()),
            }
        else:
            st.error("Unsupported file type.")
            st.stop()

        if data.get("word_count", 0) == 0:
            if os.path.exists(file_path):
                os.remove(file_path)
            st.error("No text could be extracted from this content.")
            st.stop()

        step("Saving lecture metadata...", 60)
        lecture_id = add_lecture(
            title=custom_title.strip(),
            filename=filename,
            pages=data["pages"],
            word_count=data["word_count"],
            file_hash=file_hash,
        )

        step("Writing extracted text...", 85)
        text_path = os.path.join(UPLOAD_DIR, "texts", f"{lecture_id}.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(data["text"])

        progress.progress(100)
        status.html(
            "<div class='step-item done'>✅ Processing complete</div>"
        )
        st.success(
            f"'{custom_title}' was processed successfully with "
            f"{data['pages']} page(s) and {data['word_count']:,} words."
        )
        st.info("Next: open Notes Generator to create the study materials.")

    except Exception as exc:
        progress.empty()
        status.empty()
        st.error(f"Error processing lecture: {exc}")
