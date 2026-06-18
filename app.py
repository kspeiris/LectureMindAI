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
            <div class='bg-white/5 border border-purple-500/20 rounded-xl px-4 py-3 text-center mb-2'>
              <div style='display:flex; justify-content:space-around;'>
                <div><div class='font-["Outfit"] text-2xl font-bold text-purple-400'>{lc}</div><div class='text-xs text-slate-500 uppercase tracking-wider mt-0.5'>Lectures</div></div>
                <div><div class='font-["Outfit"] text-2xl font-bold text-blue-400'>{nc}</div><div class='text-xs text-slate-500 uppercase tracking-wider mt-0.5'>Notes</div></div>
                <div><div class='font-["Outfit"] text-2xl font-bold text-emerald-400'>{fc}</div><div class='text-xs text-slate-500 uppercase tracking-wider mt-0.5'>Cards</div></div>
                <div><div class='font-["Outfit"] text-2xl font-bold text-pink-400'>{mc}</div><div class='text-xs text-slate-500 uppercase tracking-wider mt-0.5'>MCQs</div></div>
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
<div class='bg-gradient-to-br from-purple-600/20 via-indigo-600/10 to-emerald-500/10 border border-purple-500/20 rounded-[22px] px-8 py-10 text-center backdrop-blur-md mb-7 relative overflow-hidden'>
  <h1 class='font-["Outfit"] text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-emerald-400 text-5xl font-extrabold mb-3'>LectureMind AI</h1>
  <p class='text-lg text-slate-400 max-w-2xl mx-auto mb-6'>
    Transform your lecture materials into smart summaries, flashcards, MCQ quizzes,
    and an AI-powered study assistant — in minutes.
  </p>
  <div class='flex gap-3 justify-center flex-wrap'>
    <span class='inline-block bg-gradient-to-br from-purple-500/30 to-indigo-500/20 border border-purple-500/30 rounded-full px-4 py-1.5 text-sm font-medium text-purple-300 backdrop-blur-sm transition-all hover:-translate-y-px hover:shadow-lg hover:from-purple-500/50 hover:to-indigo-500/40 cursor-default'>⚡ Powered by FLAN-T5</span>
    <span class='inline-block bg-gradient-to-br from-purple-500/30 to-indigo-500/20 border border-purple-500/30 rounded-full px-4 py-1.5 text-sm font-medium text-purple-300 backdrop-blur-sm transition-all hover:-translate-y-px hover:shadow-lg hover:from-purple-500/50 hover:to-indigo-500/40 cursor-default'>🔍 RAG Knowledge Base</span>
    <span class='inline-block bg-gradient-to-br from-purple-500/30 to-indigo-500/20 border border-purple-500/30 rounded-full px-4 py-1.5 text-sm font-medium text-purple-300 backdrop-blur-sm transition-all hover:-translate-y-px hover:shadow-lg hover:from-purple-500/50 hover:to-indigo-500/40 cursor-default'>📊 Progress Analytics</span>
    <span class='inline-block bg-gradient-to-br from-purple-500/30 to-indigo-500/20 border border-purple-500/30 rounded-full px-4 py-1.5 text-sm font-medium text-purple-300 backdrop-blur-sm transition-all hover:-translate-y-px hover:shadow-lg hover:from-purple-500/50 hover:to-indigo-500/40 cursor-default'>📤 PDF & DOCX Export</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class='bg-white/5 border border-purple-500/20 rounded-2xl p-6 backdrop-blur-md shadow-xl transition-all duration-200 h-full hover:-translate-y-1 hover:shadow-2xl hover:border-purple-500/40'>
      <div class='text-4xl mb-3'>📤</div>
      <h3 class='text-slate-200 text-lg font-semibold mb-2'>Upload & Extract</h3>
      <p class='text-slate-400 text-sm leading-relaxed'>Upload PDF, PPTX, or TXT files. The system extracts and cleans text with smart artifact removal,
         duplicate detection, and custom title labelling.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='bg-white/5 border border-purple-500/20 rounded-2xl p-6 backdrop-blur-md shadow-xl transition-all duration-200 h-full hover:-translate-y-1 hover:shadow-2xl hover:border-purple-500/40'>
      <div class='text-4xl mb-3'>🧠</div>
      <h3 class='text-slate-200 text-lg font-semibold mb-2'>AI Generation</h3>
      <p class='text-slate-400 text-sm leading-relaxed'>Generates structured bullet-point summaries, diverse keyword concepts, interactive
         flashcards, and concise MCQs — all powered by FLAN-T5-Base.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='bg-white/5 border border-purple-500/20 rounded-2xl p-6 backdrop-blur-md shadow-xl transition-all duration-200 h-full hover:-translate-y-1 hover:shadow-2xl hover:border-purple-500/40'>
      <div class='text-4xl mb-3'>🤖</div>
      <h3 class='text-slate-200 text-lg font-semibold mb-2'>AI Study Assistant</h3>
      <p class='text-slate-400 text-sm leading-relaxed'>Ask any question in natural language. The RAG engine retrieves relevant passages,
         synthesises a precise answer, and shows confidence scores with source citations.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

c4, c5, c6 = st.columns(3)
with c4:
    st.markdown("""
    <div class='bg-white/5 border border-purple-500/20 rounded-2xl p-6 backdrop-blur-md shadow-xl transition-all duration-200 h-full hover:-translate-y-1 hover:shadow-2xl hover:border-purple-500/40'>
      <div class='text-4xl mb-3'>📇</div>
      <h3 class='text-slate-200 text-lg font-semibold mb-2'>Smart Flashcards</h3>
      <p class='text-slate-400 text-sm leading-relaxed'>Study with AI-generated question & answer cards. Mark cards as Known or
         Review Again — the progress bar tracks your session in real time.</p>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class='bg-white/5 border border-purple-500/20 rounded-2xl p-6 backdrop-blur-md shadow-xl transition-all duration-200 h-full hover:-translate-y-1 hover:shadow-2xl hover:border-purple-500/40'>
      <div class='text-4xl mb-3'>✍️</div>
      <h3 class='text-slate-200 text-lg font-semibold mb-2'>MCQ Quiz</h3>
      <p class='text-slate-400 text-sm leading-relaxed'>Test yourself with multiple-choice questions that have model-generated, concise
         distractors. Get a score badge and performance gauge chart instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown("""
    <div class='bg-white/5 border border-purple-500/20 rounded-2xl p-6 backdrop-blur-md shadow-xl transition-all duration-200 h-full hover:-translate-y-1 hover:shadow-2xl hover:border-purple-500/40'>
      <div class='text-4xl mb-3'>📊</div>
      <h3 class='text-slate-200 text-lg font-semibold mb-2'>Analytics Dashboard</h3>
      <p class='text-slate-400 text-sm leading-relaxed'>Track uploaded lectures, notes, flashcards, and quiz history.
         Export notes as professional PDF or DOCX documents with one click.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Workflow steps ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🚀 How to Get Started")
step_cols = st.columns(4)
steps = [
    ("1️⃣", "Upload",    "Go to **Upload Lecture** and upload a PDF, PPTX, or TXT file."),
    ("2️⃣", "Generate",  "Go to **Notes Generator** to create summaries and build the AI knowledge base."),
    ("3️⃣", "Study",     "Use **Flashcards** and **MCQ Quiz** to test your understanding."),
    ("4️⃣", "Ask AI",    "Open **AI Study Assistant** to ask questions and get cited answers."),
]
for col, (num, title, desc) in zip(step_cols, steps):
    with col:
        st.markdown(
            f"<div class='bg-white/5 border border-purple-500/20 rounded-2xl p-6 text-center backdrop-blur-md shadow-lg transition-all duration-200 h-full hover:-translate-y-1 hover:shadow-2xl hover:border-purple-500/40'>"
            f"<div class='text-3xl mb-3'>{num}</div>"
            f"<h3 class='text-slate-200 text-lg font-semibold mb-2'>{title}</h3>"
            f"<p class='text-slate-400 text-sm leading-relaxed'>{desc}</p>"
            f"</div>",
            unsafe_allow_html=True
        )
