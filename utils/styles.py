import html

import streamlit as st


PREMIUM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp, .stApp > div {
    background: linear-gradient(135deg, #100b2d 0%, #1f1a46 52%, #171433 100%) !important;
    min-height: 100vh;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: transparent !important;
}
.block-container,
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
    max-width: 1360px !important;
    padding: 1.7rem 2rem 4.5rem 2rem !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: rgba(13, 9, 36, 0.96) !important;
    border-right: 1px solid rgba(167,139,250,0.18) !important;
    backdrop-filter: blur(20px) !important;
}
[data-testid="stSidebar"] * { color: #c4b5fd !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #94a3b8 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(167,139,250,0.16) !important; }
[data-testid="stSidebarNav"] a {
    border-radius: 8px !important;
}
[data-testid="stSidebarNav"] a span {
    color: #c4b5fd !important;
    font-size: 0.9rem !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"],
[data-testid="stSidebarNav"] a:hover {
    background: rgba(167,139,250,0.16) !important;
}

h1 {
    font-family: 'Outfit', sans-serif !important;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: clamp(2rem, 3.5vw, 3.05rem) !important;
    font-weight: 800 !important;
    letter-spacing: 0 !important;
    margin-bottom: 0.2rem !important;
}
h2 {
    font-family: 'Outfit', sans-serif !important;
    color: #e2e8f0 !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
}
h3 {
    font-family: 'Outfit', sans-serif !important;
    color: #d8b4fe !important;
    font-size: 1.12rem !important;
    font-weight: 700 !important;
}
h4 { color: #cbd5e1 !important; }
p, li { color: #cbd5e1 !important; line-height: 1.7; }
a { color: #a78bfa !important; }
label { color: #94a3b8 !important; font-size: 0.88rem !important; }
small { color: #64748b !important; }
strong { color: #f8fafc !important; }
hr {
    border: none !important;
    border-top: 1px solid rgba(167,139,250,0.16) !important;
    margin: 1.25rem 0 !important;
}

[data-testid="stHorizontalBlock"] { gap: 1.25rem !important; }
[data-testid="stVerticalBlock"] { gap: 1rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    padding: 0.58rem 1.15rem !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.28) !important;
    transition: transform 0.16s ease, box-shadow 0.16s ease, background 0.16s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 12px 32px rgba(124,58,237,0.38) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.065) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    color: #cbd5e1 !important;
    box-shadow: none !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #047857, #065f46) !important;
    border: 0 !important;
    border-radius: 10px !important;
    color: #d1fae5 !important;
    font-weight: 700 !important;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.055) !important;
    border: 1px solid rgba(167,139,250,0.20) !important;
    border-radius: 16px !important;
    padding: 1.05rem 1.15rem !important;
    box-shadow: 0 12px 34px rgba(2,6,23,0.16) !important;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    font-size: 0.76rem !important;
}
[data-testid="stMetricValue"] {
    color: #c4b5fd !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
}

[data-testid="stFileUploader"] {
    background: rgba(124,58,237,0.07) !important;
    border: 1.5px dashed rgba(167,139,250,0.42) !important;
    border-radius: 16px !important;
    padding: 0.9rem !important;
}
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.065) !important;
    border: 1px solid rgba(167,139,250,0.28) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.62) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.13) !important;
}
[data-baseweb="popover"] [role="option"] {
    background: #221b4a !important;
    color: #f8fafc !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    color: #94a3b8 !important;
    font-weight: 700 !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(124,58,237,0.42) !important;
    color: #f8fafc !important;
}

.stRadio > div {
    gap: 0.45rem !important;
}
.stRadio label {
    background: rgba(255,255,255,0.035) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 0.45rem 0.7rem !important;
}
.stRadio label:hover {
    border-color: rgba(167,139,250,0.35) !important;
    background: rgba(124,58,237,0.08) !important;
}

.stAlert {
    border-radius: 12px !important;
    border-left-width: 4px !important;
}
.stProgress > div > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 999px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #8b5cf6, #38bdf8) !important;
    border-radius: 999px !important;
}
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary {
    color: #d8b4fe !important;
    font-weight: 700 !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stBottom"],
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div {
    background: rgba(13,9,36,0.96) !important;
    border-top: 1px solid rgba(167,139,250,0.16) !important;
}

::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.38); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: rgba(167,139,250,0.62); }

.lm-sidebar-brand {
    align-items: center;
    color: #c4b5fd;
    display: flex;
    font-family: 'Outfit', sans-serif;
    font-size: 1.45rem;
    font-weight: 800;
    gap: 0.65rem;
    margin-bottom: 0.25rem;
}
.lm-logo-mark {
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    border-radius: 7px;
    box-shadow: 0 8px 22px rgba(124,58,237,0.38);
    height: 22px;
    width: 22px;
}
.lm-sidebar-subtitle {
    color: #94a3b8 !important;
    font-size: 0.78rem;
    margin: 0 0 1rem 0;
}
.lm-stat-grid {
    border-bottom: 1px solid rgba(167,139,250,0.14);
    border-top: 1px solid rgba(167,139,250,0.14);
    display: grid;
    gap: 0.45rem;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    padding: 0.85rem 0;
}
.lm-stat-value {
    color: #c4b5fd;
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    text-align: center;
}
.lm-stat-label {
    color: #94a3b8;
    font-size: 0.72rem;
    text-align: center;
}
.hero-section {
    background:
        radial-gradient(circle at 12% 20%, rgba(96,165,250,0.16), transparent 34%),
        linear-gradient(135deg, rgba(124,58,237,0.22), rgba(30,27,75,0.62), rgba(16,185,129,0.10));
    border: 1px solid rgba(167,139,250,0.22);
    border-radius: 22px;
    box-shadow: 0 18px 55px rgba(2,6,23,0.24);
    margin-bottom: 1.4rem;
    padding: 2.25rem;
}
.hero-section h1 {
    font-size: clamp(2.15rem, 5vw, 3.35rem) !important;
    margin: 0 0 0.65rem 0 !important;
}
.hero-section p {
    color: #dbeafe !important;
    font-size: 1.02rem;
    margin: 0 0 1.1rem 0;
    max-width: 780px;
}
.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
}
.feature-pill,
.kw-pill {
    align-items: center;
    background: rgba(124,58,237,0.16);
    border: 1px solid rgba(167,139,250,0.26);
    border-radius: 999px;
    color: #ddd6fe !important;
    display: inline-flex;
    font-size: 0.84rem;
    font-weight: 700;
    gap: 0.4rem;
    line-height: 1.2;
    margin: 0.15rem;
    padding: 0.42rem 0.78rem;
    white-space: nowrap;
}
.premium-card,
.step-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(167,139,250,0.18);
    border-radius: 16px;
    box-shadow: 0 12px 34px rgba(2,6,23,0.18);
    min-height: 100%;
    padding: 1.35rem;
    transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
}
.premium-card:hover,
.step-card:hover {
    background: rgba(255,255,255,0.075);
    border-color: rgba(167,139,250,0.34);
    transform: translateY(-2px);
}
.feature-icon,
.step-icon {
    align-items: center;
    background: rgba(167,139,250,0.14);
    border-radius: 12px;
    color: #ddd6fe;
    display: inline-flex;
    font-size: 1.25rem;
    height: 2.25rem;
    justify-content: center;
    margin-bottom: 0.75rem;
    width: 2.25rem;
}
.premium-card h3,
.step-card h3 {
    color: #e9d5ff !important;
    font-size: 1.08rem !important;
    margin: 0 0 0.5rem 0 !important;
}
.premium-card p,
.step-card p {
    color: #cbd5e1 !important;
    font-size: 0.94rem;
    line-height: 1.65;
    margin: 0;
}
.step-card { text-align: center; }
.info-strip {
    background: rgba(96,165,250,0.10);
    border: 1px solid rgba(96,165,250,0.24);
    border-radius: 12px;
    color: #bfdbfe !important;
    font-size: 0.9rem;
    margin: 0.7rem 0 1rem 0;
    padding: 0.72rem 0.95rem;
}
.step-item {
    align-items: center;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    color: #94a3b8 !important;
    display: flex;
    font-size: 0.9rem;
    gap: 0.65rem;
    margin-bottom: 0.45rem;
    padding: 0.68rem 0.95rem;
}
.step-item.active {
    background: rgba(124,58,237,0.14);
    border-color: rgba(167,139,250,0.35);
    color: #ddd6fe !important;
}
.step-item.done {
    background: rgba(34,197,94,0.08);
    border-color: rgba(74,222,128,0.22);
    color: #86efac !important;
}
.progress-meta {
    color: #94a3b8;
    display: flex;
    font-size: 0.9rem;
    gap: 1rem;
    justify-content: space-between;
    margin-bottom: 0.45rem;
}
.progress-track {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    height: 8px;
    margin-bottom: 1.2rem;
    overflow: hidden;
    width: 100%;
}
.progress-fill {
    background: linear-gradient(90deg, #8b5cf6, #38bdf8);
    border-radius: 999px;
    height: 100%;
    transition: width 0.25s ease;
}
.flashcard-face {
    align-items: center;
    border-radius: 18px;
    box-shadow: 0 18px 44px rgba(2,6,23,0.24);
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 250px;
    padding: 2rem;
    text-align: center;
    width: 100%;
}
.flashcard-front {
    background: linear-gradient(135deg, rgba(124,58,237,0.20), rgba(59,130,246,0.11));
    border: 1px solid rgba(167,139,250,0.34);
}
.flashcard-back {
    background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(20,184,166,0.10));
    border: 1px solid rgba(52,211,153,0.34);
}
.fc-label {
    color: #c4b5fd;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    margin-bottom: 0.75rem;
}
.fc-text {
    color: #f8fafc;
    font-size: 1.12rem;
    line-height: 1.65;
}
.muted-hint {
    color: #94a3b8 !important;
    font-size: 0.82rem;
    margin-top: 0.55rem;
    text-align: center;
}
.quiz-question,
.review-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    margin-bottom: 0.75rem;
    padding: 1rem 1.15rem;
}
.review-card.ok {
    background: rgba(34,197,94,0.075);
    border-color: rgba(74,222,128,0.26);
}
.review-card.bad {
    background: rgba(248,113,113,0.075);
    border-color: rgba(248,113,113,0.28);
}
.score-badge {
    align-items: center;
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 999px;
    color: #e2e8f0 !important;
    display: inline-flex;
    font-weight: 800;
    gap: 0.5rem;
    padding: 0.62rem 1.05rem;
}
.score-badge.excellent { background: rgba(34,197,94,0.12); border-color: rgba(74,222,128,0.32); color: #86efac !important; }
.score-badge.good { background: rgba(59,130,246,0.12); border-color: rgba(96,165,250,0.32); color: #93c5fd !important; }
.score-badge.review { background: rgba(251,146,60,0.12); border-color: rgba(251,146,60,0.32); color: #fdba74 !important; }

@media (max-width: 768px) {
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .hero-section { padding: 1.35rem; }
    .pill-row,
    .progress-meta {
        flex-direction: column;
        gap: 0.45rem;
    }
}
</style>
"""


def inject_css():
    """Inject shared app styling."""
    st.html(PREMIUM_CSS)


def page_header(title: str, subtitle: str = ""):
    """Render a styled page header with optional subtitle."""
    st.html(f"<h1>{title}</h1>")
    if subtitle:
        st.html(
            f"<p style='font-size:1rem; color:#94a3b8; margin-top:-8px; margin-bottom:1rem;'>{subtitle}</p>"
        )


def keyword_pills_html(keywords: list) -> str:
    """Convert a list of keywords into styled pill badges HTML."""
    pills = "".join(
        f"<span class='kw-pill'>{html.escape(str(keyword))}</span>"
        for keyword in keywords
        if str(keyword).strip()
    )
    return f"<div style='margin:0.5rem 0 1rem 0; line-height:2.2;'>{pills}</div>" if pills else ""


def score_badge_html(score: int, total: int) -> str:
    """Return an HTML score badge based on percentage."""
    pct = (score / total * 100) if total > 0 else 0
    if pct >= 80:
        cls, icon, label = "excellent", "🏆", "Excellent!"
    elif pct >= 60:
        cls, icon, label = "good", "👍", "Good Work"
    else:
        cls, icon, label = "review", "📖", "Keep Reviewing"
    return f"<div class='score-badge {cls}'>{icon} {score}/{total} — {label} ({pct:.0f}%)</div>"
