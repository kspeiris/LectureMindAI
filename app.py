import streamlit as st
from utils.styles import inject_css

st.set_page_config(
    page_title='LectureMind AI',
    page_icon='📚',
    layout='wide',
    initial_sidebar_state='expanded'
)

inject_css()

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='font-family:Outfit,sans-serif; background:linear-gradient(90deg,#a78bfa,#60a5fa);"
        "-webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0;'>"
        "📚 LectureMind AI</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:0.78rem; color:#64748b; margin-top:0; margin-bottom:1rem;'>"
        "AI-Powered Study Assistant</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Quick stats
    try:
        from database.database import get_lecture_count, get_flashcards_count, get_mcq_count, get_notes_count
        lc, fc, mc, nc = get_lecture_count(), get_flashcards_count(), get_mcq_count(), get_notes_count()
        st.markdown(
            f"""
            <div class='stat-mini' style='margin-bottom:0.5rem;'>
              <div style='display:flex; justify-content:space-around;'>
                <div><div class='stat-val'>{lc}</div><div class='stat-label'>Lectures</div></div>
                <div><div class='stat-val' style='color:#60a5fa;'>{nc}</div><div class='stat-label'>Notes</div></div>
                <div><div class='stat-val' style='color:#34d399;'>{fc}</div><div class='stat-label'>Cards</div></div>
                <div><div class='stat-val' style='color:#f472b6;'>{mc}</div><div class='stat-label'>MCQs</div></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception:
        st.markdown("<small style='color:#475569;'>Upload a lecture to get started!</small>",
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<small style='color:#475569;'>Navigate using the pages menu above ↑</small>",
        unsafe_allow_html=True
    )

# ── Hero Section ──────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-section'>
  <h1 style='font-size:3rem !important; margin-bottom:0.6rem;'>LectureMind AI</h1>
  <p style='font-size:1.15rem; color:#94a3b8; max-width:600px; margin:0 auto 1.5rem auto;'>
    Transform your lecture materials into smart summaries, flashcards, MCQ quizzes,
    and an AI-powered study assistant — in minutes.
  </p>
  <div style='display:flex; gap:0.8rem; justify-content:center; flex-wrap:wrap;'>
    <span class='kw-pill' style='font-size:0.88rem;'>⚡ Powered by FLAN-T5</span>
    <span class='kw-pill' style='font-size:0.88rem;'>🔍 RAG Knowledge Base</span>
    <span class='kw-pill' style='font-size:0.88rem;'>📊 Progress Analytics</span>
    <span class='kw-pill' style='font-size:0.88rem;'>📤 PDF & DOCX Export</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class='premium-card'>
      <div style='font-size:2.2rem; margin-bottom:0.7rem;'>📤</div>
      <h3>Upload & Extract</h3>
      <p>Upload PDF or PPTX files. The system extracts and cleans text with smart artifact removal,
         duplicate detection, and custom title labelling.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='premium-card'>
      <div style='font-size:2.2rem; margin-bottom:0.7rem;'>🧠</div>
      <h3>AI Generation</h3>
      <p>Generates structured bullet-point summaries, diverse keyword concepts, interactive
         flashcards, and concise MCQs — all powered by FLAN-T5-Base.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='premium-card'>
      <div style='font-size:2.2rem; margin-bottom:0.7rem;'>🤖</div>
      <h3>AI Study Assistant</h3>
      <p>Ask any question in natural language. The RAG engine retrieves relevant passages,
         synthesises a precise answer, and shows confidence scores with source citations.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

c4, c5, c6 = st.columns(3)
with c4:
    st.markdown("""
    <div class='premium-card'>
      <div style='font-size:2.2rem; margin-bottom:0.7rem;'>📇</div>
      <h3>Smart Flashcards</h3>
      <p>Study with AI-generated question & answer cards. Mark cards as Known or
         Review Again — the progress bar tracks your session in real time.</p>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class='premium-card'>
      <div style='font-size:2.2rem; margin-bottom:0.7rem;'>✍️</div>
      <h3>MCQ Quiz</h3>
      <p>Test yourself with multiple-choice questions that have model-generated, concise
         distractors. Get a score badge and performance gauge chart instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown("""
    <div class='premium-card'>
      <div style='font-size:2.2rem; margin-bottom:0.7rem;'>📊</div>
      <h3>Analytics Dashboard</h3>
      <p>Track uploaded lectures, notes, flashcards, and quiz history.
         Export notes as professional PDF or DOCX documents with one click.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Workflow steps ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🚀 How to Get Started")
step_cols = st.columns(4)
steps = [
    ("1️⃣", "Upload",    "Go to **Upload Lecture** and upload a PDF or PPTX file."),
    ("2️⃣", "Generate",  "Go to **Notes Generator** to create summaries and build the AI knowledge base."),
    ("3️⃣", "Study",     "Use **Flashcards** and **MCQ Quiz** to test your understanding."),
    ("4️⃣", "Ask AI",    "Open **AI Study Assistant** to ask questions and get cited answers."),
]
for col, (num, title, desc) in zip(step_cols, steps):
    with col:
        st.markdown(
            f"<div class='premium-card' style='text-align:center;'>"
            f"<div style='font-size:1.8rem;'>{num}</div>"
            f"<h3>{title}</h3>"
            f"<p style='font-size:0.88rem;'>{desc}</p>"
            f"</div>",
            unsafe_allow_html=True
        )
