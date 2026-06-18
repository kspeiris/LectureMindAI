import streamlit as st

from utils.styles import inject_css

st.set_page_config(
    page_title="LectureMind AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

with st.sidebar:
    st.html(
        """
        <div class="lm-sidebar-brand">
            <span class="lm-logo-mark"></span>
            <span>LectureMind AI</span>
        </div>
        <p class="lm-sidebar-subtitle">AI-powered study assistant</p>
        """
    )
    st.markdown("---")

    try:
        from database.database import (
            get_flashcards_count,
            get_lecture_count,
            get_mcq_count,
            get_notes_count,
        )

        lc = get_lecture_count()
        fc = get_flashcards_count()
        mc = get_mcq_count()
        nc = get_notes_count()
        st.html(
            f"""
            <div class="lm-stat-grid">
                <div><div class="lm-stat-value">{lc}</div><div class="lm-stat-label">Lectures</div></div>
                <div><div class="lm-stat-value">{nc}</div><div class="lm-stat-label">Notes</div></div>
                <div><div class="lm-stat-value">{fc}</div><div class="lm-stat-label">Cards</div></div>
                <div><div class="lm-stat-value">{mc}</div><div class="lm-stat-label">MCQs</div></div>
            </div>
            """
        )
    except Exception:
        st.caption("Upload a lecture to get started.")

    st.caption("Navigate using the pages menu above.")

st.html(
    """
    <section class="hero-section">
        <h1>LectureMind AI</h1>
        <p>
            Transform lecture materials into summaries, flashcards, MCQ quizzes,
            exports, analytics, and a searchable AI study assistant.
        </p>
        <div class="pill-row">
            <span class="feature-pill">⚡ FLAN-T5 generation</span>
            <span class="feature-pill">🔎 RAG knowledge base</span>
            <span class="feature-pill">📊 Progress analytics</span>
            <span class="feature-pill">📄 PDF and DOCX export</span>
        </div>
    </section>
    """
)

features = [
    (
        "📤",
        "Upload & Extract",
        "Upload PDF, PPTX, or TXT files. The app extracts clean text, detects duplicates, and keeps lecture titles organized.",
    ),
    (
        "🧠",
        "AI Generation",
        "Generate structured summaries, keyword concepts, flashcards, and concise MCQs from lecture content.",
    ),
    (
        "🤖",
        "AI Study Assistant",
        "Ask natural-language questions and get answers grounded in retrieved lecture passages with relevance scores.",
    ),
    (
        "📇",
        "Smart Flashcards",
        "Practice active recall with question-and-answer cards, known/review tracking, and session progress.",
    ),
    (
        "✅",
        "MCQ Quiz",
        "Test understanding with multiple-choice questions, instant scoring, and answer review.",
    ),
    (
        "📊",
        "Analytics Dashboard",
        "Track lectures, notes, flashcards, quiz history, and generated study resources from one overview.",
    ),
]

top = st.columns(3)
bottom = st.columns(3)
for col, (icon, title, body) in zip(top + bottom, features):
    with col:
        st.html(
            f"""
            <div class="premium-card">
                <div class="feature-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{body}</p>
            </div>
            """
        )

st.markdown("---")
st.markdown("### 🚀 How to Get Started")

steps = [
    ("1", "Upload", "Add a PDF, PPTX, TXT file, or paste lecture text."),
    ("2", "Generate", "Create summaries, keywords, and the searchable knowledge base."),
    ("3", "Study", "Review notes, flashcards, and MCQ quizzes."),
    ("4", "Ask AI", "Use the study assistant for lecture-specific questions."),
]

for col, (num, title, desc) in zip(st.columns(4), steps):
    with col:
        st.html(
            f"""
            <div class="step-card">
                <div class="step-icon">{num}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """
        )
