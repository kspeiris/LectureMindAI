import streamlit as st
import os
import plotly.graph_objects as go
from database.database import get_all_lectures, get_mcqs, save_mcqs, save_quiz_result
from models.mcq_generator import generate_mcqs
from utils.styles import inject_css, page_header, score_badge_html

inject_css()
page_header("✍️ MCQ Quiz", "Test your knowledge with AI-generated multiple-choice questions.")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload a lecture first.")
    st.stop()

options = {lec['id']: lec['title'] for lec in lectures}
selected_id = st.selectbox(
    "Select Lecture for Quiz",
    options=list(options.keys()),
    format_func=lambda x: options[x]
)

mcqs = get_mcqs(selected_id)

# ── No MCQs yet ───────────────────────────────────────────────────────────
if not mcqs:
    st.info("No MCQs found for this lecture.")
    num_q = st.slider("How many questions to generate?", 3, 15, 8)
    if st.button("✨ Generate MCQs", use_container_width=False):
        text_path = os.path.join(
            os.path.dirname(__file__), '..', 'uploads', 'texts', f"{selected_id}.txt"
        )
        if os.path.exists(text_path):
            with st.spinner("Generating questions using AI…"):
                with open(text_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                new_mcqs = generate_mcqs(text, num_mcqs=num_q)
                save_mcqs(selected_id, new_mcqs)
            st.success(f"✅ {len(new_mcqs)} MCQs generated!")
            st.rerun()
        else:
            st.error("Source text not found. Please re-upload the lecture.")
    st.stop()

# ── Quiz UI ───────────────────────────────────────────────────────────────
st.markdown(f"### 📋 Test Your Knowledge — {len(mcqs)} Questions")
st.html(
    "<div class='info-strip'>Select one answer per question, then click <strong>Submit Quiz</strong>.</div>"
)
st.write("")

with st.form("quiz_form"):
    user_answers = {}
    for i, mcq in enumerate(mcqs):
        opts = [mcq.get('option_a',''), mcq.get('option_b',''),
                mcq.get('option_c',''), mcq.get('option_d','')]
        opts = [o for o in opts if o.strip()]

        st.html(
            f"<div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);"
            f"border-radius:12px; padding:1rem 1.2rem; margin-bottom:0.6rem;'>"
            f"<strong style='color:#e2e8f0;'>Q{i+1}:</strong> "
            f"<span style='color:#cbd5e1;'>{mcq['question']}</span></div>"
        )
        user_answers[i] = st.radio(
            f"q_{i+1}",
            options=opts,
            key=f"q_{i}",
            label_visibility="collapsed",
            index=None
        )
        st.write("")

    submitted = st.form_submit_button("🚀 Submit Quiz", use_container_width=False)

# ── Results ───────────────────────────────────────────────────────────────
if submitted:
    # Validate that all questions were answered
    missing = [i + 1 for i in range(len(mcqs)) if user_answers.get(i) is None]
    if missing:
        st.error(f"⚠️ Please answer all questions before submitting. Missing questions: {', '.join(map(str, missing))}")
        st.stop()

    score = sum(
        1 for i, mcq in enumerate(mcqs)
        if user_answers.get(i) == mcq.get('correct_answer')
    )
    total = len(mcqs)
    pct   = score / total * 100 if total > 0 else 0

    save_quiz_result(selected_id, score, total)

    st.markdown("---")
    st.markdown("### 🏆 Your Result")

    # Score badge
    st.html(score_badge_html(score, total))
    st.write("")

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode  = "gauge+number",
        value = pct,
        number= {"suffix": "%", "font": {"size": 36, "color": "#e2e8f0", "family": "Outfit"}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569",
                     'tickfont': {'color': '#94a3b8'}},
            'bar':  {'color': "#7c3aed"},
            'bgcolor': "rgba(255,255,255,0.04)",
            'borderwidth': 0,
            'steps': [
                {'range': [0,  60], 'color': 'rgba(251,146,60,0.15)'},
                {'range': [60, 80], 'color': 'rgba(96,165,250,0.15)'},
                {'range': [80,100], 'color': 'rgba(52,211,153,0.15)'},
            ],
            'threshold': {
                'line':  {'color': "#a78bfa", 'width': 3},
                'thickness': 0.85,
                'value': pct,
            },
        },
        title = {'text': "Score", 'font': {'color': '#94a3b8', 'size': 14}},
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=260,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family="Inter"),
    )
    _, gauge_col, _ = st.columns([1, 3, 1])
    with gauge_col:
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Answer Review ─────────────────────────────────────────────────────
    with st.expander("📖 Review Answers", expanded=True):
        for i, mcq in enumerate(mcqs):
            correct = mcq.get('correct_answer', '')
            chosen  = user_answers.get(i, '')
            is_right = (chosen == correct)

            border_color = "rgba(52,211,153,0.35)" if is_right else "rgba(248,113,113,0.35)"
            bg_color     = "rgba(52,211,153,0.06)"  if is_right else "rgba(248,113,113,0.06)"
            icon         = "✅" if is_right else "❌"

            ans_color = "#34d399" if is_right else "#f87171"
            st.html(
                f"<div style='background:{bg_color}; border:1px solid {border_color};"
                f"border-radius:12px; padding:1rem 1.2rem; margin-bottom:0.7rem;'>"
                f"<strong style='color:#e2e8f0;'>{icon} Q{i+1}: {mcq['question']}</strong><br>"
                f"<span style='color:#94a3b8;'>Your answer: </span>"
                f"<span style='color:{ans_color};'><strong>{chosen}</strong></span>"
            )
            if not is_right:
                st.html(
                    f"<span style='color:#94a3b8;'> &nbsp;·&nbsp; Correct: </span>"
                    f"<span style='color:#34d399;'><strong>{correct}</strong></span>"
                )
            st.html("</div>")

    # ── Regenerate ────────────────────────────────────────────────────────
    st.write("")
    if st.button("🔄 Regenerate Questions", use_container_width=False):
        text_path = os.path.join(
            os.path.dirname(__file__), '..', 'uploads', 'texts', f"{selected_id}.txt"
        )
        if os.path.exists(text_path):
            with st.spinner("Generating new questions…"):
                with open(text_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                new_mcqs = generate_mcqs(text, num_mcqs=len(mcqs))
                save_mcqs(selected_id, new_mcqs)
            st.success("New questions generated!")
            st.rerun()
