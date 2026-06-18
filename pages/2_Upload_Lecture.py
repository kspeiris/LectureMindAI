import streamlit as st
import os
import hashlib
from services.pdf_processor import extract_text_from_pdf
from services.ppt_processor import extract_text_from_ppt
from database.database import add_lecture, check_duplicate_file
from utils.styles import inject_css, page_header

inject_css()
page_header("📤 Upload Lecture",
            "Upload PDF, PPTX, or TXT lecture files to start generating intelligent study aids.")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(os.path.join(UPLOAD_DIR, 'pdfs'),  exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'pptx'),  exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'texts'), exist_ok=True)

# ── Input Method ──────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📄 Upload File", "📝 Paste Text"])

with tab1:
    uploaded_file = st.file_uploader(
        "Choose a lecture file",
        type=["pdf", "pptx", "txt"],
        help="Supported formats: PDF, PowerPoint (PPTX), Text (TXT)"
    )

with tab2:
    pasted_text = st.text_area(
        "Paste your lecture text here",
        height=200,
        placeholder="Paste notes, transcripts, or articles here..."
    )

if uploaded_file is not None or pasted_text.strip():
    if uploaded_file is not None and pasted_text.strip():
        st.warning("⚠️ Please use either File Upload or Paste Text, but not both at the same time.")
        st.stop()

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        source_label = "File"
    else:
        file_bytes = pasted_text.encode('utf-8')
        filename = "pasted_text.txt"
        source_label = "Pasted Text"

    file_hash  = hashlib.md5(file_bytes).hexdigest()
    file_ext   = filename.split('.')[-1].lower()
    file_size_kb = len(file_bytes) / 1024

    # ── File preview info ─────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class='bg-blue-400/10 border border-blue-400/20 rounded-lg px-4 py-2.5 text-blue-300 text-sm mb-3'>
        📄 <strong>{filename if uploaded_file else "Pasted Text"}</strong> &nbsp;·&nbsp;
        {file_size_kb:.1f} KB &nbsp;·&nbsp;
        {source_label}
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
    if uploaded_file is not None:
        suggested_title = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
    else:
        suggested_title = "Pasted Notes"
        
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
        if not uploaded_file:
            filename = f"pasted_{file_hash[:8]}.txt"
            
        save_dir = 'texts' if file_ext == 'txt' else file_ext + 's'
        file_path = os.path.join(UPLOAD_DIR, save_dir, filename)
        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # ── Processing with step indicators ──────────────────────────────
        progress = st.progress(0)
        status   = st.empty()

        def step(msg, pct):
            status.markdown(
                f"<div class='flex items-center gap-3 px-4 py-2 rounded-lg mb-1.5 text-sm text-purple-400 bg-purple-500/10 border border-purple-500/30 animate-pulse'>⏳ &nbsp; {msg}</div>",
                unsafe_allow_html=True
            )
            progress.progress(pct)

        def done(msg):
            status.markdown(
                f"<div class='flex items-center gap-3 px-4 py-2 rounded-lg mb-1.5 text-sm text-emerald-400 bg-emerald-400/5 border border-emerald-400/20'>✅ &nbsp; {msg}</div>",
                unsafe_allow_html=True
            )

        try:
            step("Extracting text from document…", 20)
            if file_ext == "pdf":
                data = extract_text_from_pdf(file_path)
            elif file_ext == "pptx":
                data = extract_text_from_ppt(file_path)
            elif file_ext == "txt":
                text_content = file_bytes.decode("utf-8", errors="ignore")
                data = {
                    "text": text_content,
                    "pages": 1,
                    "word_count": len(text_content.split())
                }
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
                filename   = filename,
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
