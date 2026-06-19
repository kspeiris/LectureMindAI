import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from database.database import (
    get_lecture_count, get_flashcards_count, get_mcq_count,
    get_notes_count, get_all_lectures, get_all_quiz_results, delete_lecture
)
from utils.styles import inject_css, page_header

inject_css()
page_header("📊 Learning Dashboard", "Track your study progress at a glance")
st.markdown("---")

lec_count  = get_lecture_count()
fc_count   = get_flashcards_count()
mcq_count  = get_mcq_count()
notes_count = get_notes_count()

# ── Total words read estimate ─────────────────────────────────────────────
lectures = get_all_lectures()
total_words = sum(lec.get('word_count', 0) for lec in lectures)
reading_mins = max(0, round(total_words / 200))   # avg 200 wpm

# ── KPI Row ───────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📚 Lectures",      lec_count)
c2.metric("📝 Notes Sets",    notes_count)
c3.metric("📇 Flashcards",    fc_count)
c4.metric("✍️ MCQs",          mcq_count)
c5.metric("⏱️ Reading Saved", f"{reading_mins} min",
          help="Estimated reading time from all uploaded lectures")

st.markdown("---")

col_left, col_right = st.columns(2)

# ── Content Distribution Bar Chart ───────────────────────────────────────
with col_left:
    st.markdown("### 📊 Content Overview")
    df = pd.DataFrame({
        'Resource': ['Lectures', 'Notes', 'Flashcards', 'MCQs'],
        'Count':    [lec_count, notes_count, fc_count, mcq_count],
    })
    fig = px.bar(
        df, x='Resource', y='Count',
        color='Resource',
        color_discrete_map={
            'Lectures':   '#a78bfa',
            'Notes':      '#60a5fa',
            'Flashcards': '#34d399',
            'MCQs':       '#f472b6',
        },
        template='plotly_dark',
        title="Generated Resources",
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        showlegend=False,
        font=dict(family="Inter", color="#cbd5e1"),
        title_font=dict(size=15, color="#e2e8f0"),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(title="", gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title="Count", gridcolor='rgba(255,255,255,0.05)'),
    )
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)  # noqa: deprecated but compatible

# ── Quiz Performance Chart ────────────────────────────────────────────────
with col_right:
    st.markdown("### 🏆 Quiz Performance")
    all_results = get_all_quiz_results()
    if all_results:
        df_quiz = pd.DataFrame(all_results)
        df_quiz['Score (%)'] = (df_quiz['score'] / df_quiz['total_questions'] * 100).round(1)
        df_quiz['Lecture'] = df_quiz['lecture_title'].apply(
            lambda t: t[:22] + '…' if len(t) > 22 else t
        )
        df_quiz['Date'] = pd.to_datetime(df_quiz['taken_at']).dt.strftime('%b %d')

        fig2 = px.line(
            df_quiz, x='Date', y='Score (%)',
            color='Lecture',
            markers=True,
            template='plotly_dark',
            title="Quiz Scores Over Time",
            line_shape='spline',
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.03)',
            font=dict(family="Inter", color="#cbd5e1"),
            title_font=dict(size=15, color="#e2e8f0"),
            margin=dict(l=10, r=10, t=40, b=10),
            yaxis=dict(range=[0, 105], gridcolor='rgba(255,255,255,0.05)', title="Score %"),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        )
        fig2.update_traces(line_width=2.5, marker_size=7)
        st.plotly_chart(fig2, use_container_width=True)  # noqa: deprecated but compatible
    else:
        st.info("📊 Take a quiz to see your performance history here!")

st.markdown("---")

# ── Quiz History Table ────────────────────────────────────────────────────
all_results = get_all_quiz_results()
if all_results:
    st.markdown("### 🗒️ Quiz History")
    df_hist = pd.DataFrame(all_results)
    df_hist['Score (%)'] = (df_hist['score'] / df_hist['total_questions'] * 100).round(1)
    df_hist['Grade'] = df_hist['Score (%)'].apply(
        lambda p: "🏆 Excellent" if p >= 80 else ("👍 Good" if p >= 60 else "📖 Review")
    )
    df_hist['Date'] = pd.to_datetime(df_hist['taken_at']).dt.strftime('%Y-%m-%d %H:%M')
    display_cols = ['lecture_title', 'score', 'total_questions', 'Score (%)', 'Grade', 'Date']
    df_hist = df_hist[display_cols].rename(columns={
        'lecture_title': 'Lecture', 'score': 'Score', 'total_questions': 'Total Qs'
    })
    st.dataframe(df_hist, use_container_width=True, hide_index=True)  # noqa

st.markdown("---")

# ── Uploaded Lectures Table with Delete ──────────────────────────────────
if lectures:
    st.markdown("### 📚 Uploaded Lectures")
    for lec in lectures:
        with st.container():
            col_info, col_del = st.columns([5, 1])
            with col_info:
                st.html(
                    f"<strong>{lec['title']}</strong> &nbsp;&nbsp;"
                    f"<small style='color:#64748b;'>"
                    f"{lec.get('pages', 0)} pages · {lec.get('word_count', 0):,} words · "
                    f"Uploaded {lec.get('upload_date', '')[:10]}"
                    f"</small>"
                )
            with col_del:
                if st.button("🗑️ Delete", key=f"del_{lec['id']}",
                             help="Delete this lecture and all its data"):
                    # Also remove text file
                    text_path = os.path.join(
                        os.path.dirname(__file__), '..', 'uploads', 'texts', f"{lec['id']}.txt"
                    )
                    if os.path.exists(text_path):
                        os.remove(text_path)
                    delete_lecture(lec['id'])
                    st.success(f"Deleted '{lec['title']}'")
                    st.rerun()
        st.html("<hr style='margin:0.3rem 0; border-color:rgba(255,255,255,0.05);'>")
