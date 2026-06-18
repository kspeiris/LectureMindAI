import streamlit as st
import os
import hashlib
from services.pdf_processor import extract_text_from_pdf
from services.ppt_processor import extract_text_from_ppt
from database.database import add_lecture, check_duplicate_file
from utils.styles import inject_css, page_header

inject_css()
page_header("📤 Upload Lecture",
            "Upload PDF or PPTX lecture files to start generating intelligent study aids.")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(os.path.join(UPLOAD_DIR, 'pdfs'),  exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'pptx'),  exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'texts'), exist_ok=True)

# ── Upload widget ─────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Choose a lecture file",
    type=["pdf", "pptx"],
    help="Supported formats: PDF, PowerPoint (PPTX)"
)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_hash  = hashlib.md5(file_bytes).hexdigest()
    file_ext   = uploaded_file.name.split('.')[-1].lower()
    file_size_kb = len(file_bytes) / 1024

    # ── File preview info ─────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class='info-strip'>
        📄 <strong>{uploaded_file.name}</strong> &nbsp;·&nbsp;
        {file_size_kb:.1f} KB &nbsp;·&nbsp;
        {file_ext.upper()} file
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")

    # ── Duplicate detection ───────────────────────────────────────────────
    existing = check_duplicate_file(file_hash)
    if existing:
        st.warning(
            f"⚠️ **Duplicate detected!** This file was already uploaded as "
            f"**'{existing['title']}'** on {existing['upload_date'][:10]}. "
            f"Uploading again will create a new separate entry."
        )

    # ── Custom title input ────────────────────────────────────────────────
    suggested_title = uploaded_file.name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
    custom_title = st.text_input(
        "📝 Lecture Title",
        value=suggested_title,
        placeholder="Give this lecture a meaningful name…",
        help="This title appears across all modules — make it descriptive!"
    )

    st.write("")
    process_btn = st.button("⚙️ Process Document", use_container_width=False)

    if process_btn:
        if not custom_title.strip():
            st.error("Please enter a title for this lecture.")
            st.stop()

        # ── Save file ─────────────────────────────────────────────────────
        file_path = os.path.join(UPLOAD_DIR, file_ext + 's', uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # ── Processing with step indicators ──────────────────────────────
        progress = st.progress(0)
        status   = st.empty()

        def step(msg, pct):
            status.markdown(
                f"<div class='step-item active'>⏳ &nbsp; {msg}</div>",
                unsafe_allow_html=True
            )
            progress.progress(pct)

        def done(msg):
            status.markdown(
                f"<div class='step-item done'>✅ &nbsp; {msg}</div>",
                unsafe_allow_html=True
            )

        try:
            step("Extracting text from document…", 20)
            if file_ext == "pdf":
                data = extract_text_from_pdf(file_path)
            elif file_ext == "pptx":
                data = extract_text_from_ppt(file_path)
            else:
                st.error("Unsupported file type.")
                st.stop()

            if data.get('word_count', 0) == 0:
                st.error("❌ No text could be extracted from this file. This usually means it's an image-only PDF without OCR, or an empty document. Please upload a file containing actual text.")
                # Clean up the saved file
                if os.path.exists(file_path):
                    os.remove(file_path)
                st.stop()

            step("Saving to database…", 60)
            lecture_id = add_lecture(
                title      = custom_title.strip(),
                filename   = uploaded_file.name,
                pages      = data['pages'],
                word_count = data['word_count'],
                file_hash  = file_hash,
            )

            step("Writing extracted text…", 85)
            text_path = os.path.join(UPLOAD_DIR, 'texts', f"{lecture_id}.txt")
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(data['text'])

            progress.progress(100)
            done("Processing complete!")
            st.success(
                f"✅ **'{custom_title}'** processed successfully! "
                f"Extracted **{data['pages']} pages** and **{data['word_count']:,} words**."
            )
            st.info(
                "👉 **Next step:** Go to **Notes Generator** to create a summary, "
                "or **AI Study Assistant** to start chatting with this lecture."
            )

        except Exception as e:
            progress.empty()
            status.empty()
            st.error(f"❌ Error processing document: {str(e)}")
