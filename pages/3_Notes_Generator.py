import streamlit as st
import os
from database.database import get_all_lectures, save_notes, get_notes
from models.summarizer import generate_summary
from models.keyword_extractor import extract_keywords
from models.rag_engine import build_faiss_index
from utils.styles import inject_css, page_header

inject_css()
page_header("⚙️ Notes Generator",
            "Generate AI-powered summaries, keywords, and build the knowledge base.")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload a lecture first.")
else:
    options = {lec['id']: lec['title'] for lec in lectures}
    selected_id = st.selectbox(
        "Select a lecture",
        options=list(options.keys()),
        format_func=lambda x: options[x]
    )

    existing_notes = get_notes(selected_id)

    if existing_notes:
        st.html(
            "<div class='info-strip'>📝 Notes already exist for this lecture. "
            "Click <strong>Regenerate</strong> to refresh them with the latest AI models.</div>"
        )
        btn_label = "🔄 Regenerate Notes & Re-index"
    else:
        btn_label = "✨ Generate Smart Notes & Index"

    st.write("")

    if st.button(btn_label, use_container_width=False):
        text_path = os.path.join(
            os.path.dirname(__file__), '..', 'uploads', 'texts', f"{selected_id}.txt"
        )
        if not os.path.exists(text_path):
            st.error("❌ Source text not found. Please re-upload the lecture.")
            st.stop()

        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # ── Step-by-step progress ──────────────────────────────────────────
        progress = st.progress(0)

        steps = [
            ("📝 Generating structured summary with AI…",  15),
            ("🔑 Extracting key concepts and keywords…",   50),
            ("🧠 Building FAISS knowledge base for AI chat…", 80),
            ("💾 Saving to database…",                    95),
        ]

        step_placeholders = [st.empty() for _ in steps]

        def render_steps(active_idx: int):
            for i, (msg, _) in enumerate(steps):
                if i < active_idx:
                    step_placeholders[i].html(
                        f"<div class='step-item done'>✅ &nbsp; {msg}</div>"
                    )
                elif i == active_idx:
                    step_placeholders[i].html(
                        f"<div class='step-item active'>⏳ &nbsp; {msg}</div>"
                    )
                else:
                    step_placeholders[i].html(
                        f"<div class='step-item'>⬜ &nbsp; {msg}</div>"
                    )

        try:
            render_steps(0)
            progress.progress(15)
            with st.spinner("🤖 AI is reading the lecture and synthesising a summary…"):
                summary = generate_summary(text)

            render_steps(1)
            progress.progress(50)
            with st.spinner("🔑 Extracting the most important concepts…"):
                keywords = extract_keywords(text)

            render_steps(2)
            progress.progress(80)
            with st.spinner("🧠 Building vector knowledge base for smart search…"):
                build_faiss_index(selected_id, text)

            render_steps(3)
            progress.progress(95)
            save_notes(selected_id, summary, keywords)

            progress.progress(100)
            render_steps(len(steps))   # mark all done

            st.success(
                "🎉 **Notes generated successfully!** "
                "View them in **Notes Viewer** or start chatting in **AI Study Assistant**."
            )

        except Exception as e:
            st.error(f"❌ Error during generation: {str(e)}")
