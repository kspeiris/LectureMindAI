import streamlit as st

PREMIUM_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>

/* ===== BASE ===== */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ===== APP BACKGROUND ===== */
.stApp, .stApp > div {
    background: linear-gradient(135deg, #1a153a 0%, #231d4b 50%, #1e1940 100%) !important;
    min-height: 100vh;
}

/* Fix the white block container that Streamlit adds */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container,
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1200px !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: rgba(15, 12, 41, 0.92) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(124,58,237,0.2) !important;
}
[data-testid="stSidebar"] * { color: #c4b5fd !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #94a3b8 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(124,58,237,0.2) !important; }
[data-testid="stSidebarNav"] a span { color: #c4b5fd !important; }
[data-testid="stSidebarNav"] a[aria-selected="true"] span {
    color: #a78bfa !important;
    font-weight: 600 !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(124,58,237,0.15) !important;
    border-radius: 8px;
}

/* ===== CHAT INPUT FOOTER (white area / gap fix) ===== */
/* Kill the big bottom padding that Streamlit adds to make room for the sticky input */
[data-testid="stMainBlockContainer"],
.block-container {
    padding-bottom: 5rem !important;
}

/* The sticky footer wrapper — make it fully dark */
[data-testid="stChatInputContainer"],
[data-testid="stBottom"],
.stBottom,
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stChatInputContainer"] > div {
    background: rgba(20, 16, 48, 0.97) !important;
    backdrop-filter: blur(20px) !important;
    border-top: 1px solid rgba(124,58,237,0.18) !important;
    padding: 0.75rem 2rem !important;
}
.stChatInput, .stChatInput > div {
    background: transparent !important;
}
.stChatInput textarea,
[data-testid="stChatInputTextArea"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(124,58,237,0.35) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
.stChatInput textarea:focus,
[data-testid="stChatInputTextArea"]:focus {
    border-color: rgba(124,58,237,0.65) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
    outline: none !important;
}

/* ===== STARTER CHIP BUTTONS (AI chat page) ===== */
/* Target the small chip buttons that appear before any chat message */
[data-testid="stHorizontalBlock"] .stButton > button[kind="secondary"] {
    background: rgba(124,58,237,0.12) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 20px !important;
    color: #c4b5fd !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.75rem !important;
    box-shadow: none !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    text-align: center !important;
}
[data-testid="stHorizontalBlock"] .stButton > button[kind="secondary"]:hover {
    background: rgba(124,58,237,0.28) !important;
    border-color: rgba(124,58,237,0.55) !important;
    color: #e2e8f0 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 10px rgba(124,58,237,0.2) !important;
}

/* ===== HEADINGS ===== */
h1 {
    font-family: 'Outfit', sans-serif !important;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.2rem !important;
    letter-spacing: -0.5px;
}
h2 {
    font-family: 'Outfit', sans-serif !important;
    color: #e2e8f0 !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin-top: 0.5rem !important;
}
h3 {
    font-family: 'Outfit', sans-serif !important;
    color: #c4b5fd !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    margin-top: 0.5rem !important;
}
h4 { font-family: 'Outfit', sans-serif !important; color: #94a3b8 !important; }
p, li { color: #cbd5e1 !important; line-height: 1.7; }
a { color: #a78bfa !important; }
label { color: #94a3b8 !important; font-size: 0.88rem !important; }
small { color: #64748b !important; }
strong { color: #e2e8f0 !important; }

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(124,58,237,0.25) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.4rem !important;
    backdrop-filter: blur(12px) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, #7c3aed, #60a5fa);
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(124,58,237,0.2) !important;
    border-color: rgba(124,58,237,0.4) !important;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stMetricValue"] {
    color: #a78bfa !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.3rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 3px 12px rgba(124,58,237,0.3) !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.45) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }
/* Delete / secondary buttons */
.stButton > button[kind="secondary"],
.stButton > button.secondary {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    box-shadow: none !important;
    color: #94a3b8 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(248,113,113,0.5) !important;
    color: #f87171 !important;
}

/* ===== DOWNLOAD BUTTON ===== */
.stDownloadButton > button {
    background: linear-gradient(135deg, #065f46, #047857) !important;
    color: #d1fae5 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 3px 12px rgba(16,185,129,0.25) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(16,185,129,0.35) !important;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] {
    background: rgba(124,58,237,0.06) !important;
    border: 2px dashed rgba(124,58,237,0.4) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    transition: border-color 0.3s, background 0.3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(124,58,237,0.7) !important;
    background: rgba(124,58,237,0.08) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] { color: #94a3b8 !important; }

/* ===== SELECT BOX ===== */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stSelectbox > div > div:hover {
    border-color: rgba(124,58,237,0.55) !important;
}
/* Dropdown options */
[data-baseweb="popover"] [role="option"] {
    background: #231d4b !important;
    color: #e2e8f0 !important;
}
[data-baseweb="popover"] [role="option"]:hover {
    background: rgba(124,58,237,0.25) !important;
}

/* ===== TEXT INPUT ===== */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    padding: 0.6rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(124,58,237,0.65) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
    outline: none !important;
}

/* ===== TEXT AREA ===== */
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ===== NUMBER INPUT ===== */
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ===== SLIDER ===== */
.stSlider [data-baseweb="slider"] div {
    background: rgba(124,58,237,0.35) !important;
}
.stSlider [role="slider"] { background: #a78bfa !important; }
.stSlider > label { color: #94a3b8 !important; }

/* ===== CHAT MESSAGES ===== */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    margin-bottom: 0.6rem !important;
    padding: 0.8rem 1rem !important;
    backdrop-filter: blur(8px) !important;
}
/* User message */
[data-testid="stChatMessage"][data-testid*="user"] {
    background: rgba(124,58,237,0.1) !important;
    border-color: rgba(124,58,237,0.2) !important;
}

/* ===== EXPANDERS ===== */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    color: #c4b5fd !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(124,58,237,0.3) !important;
}

/* ===== ALERTS ===== */
.stAlert {
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
    border-left-width: 4px !important;
}
[data-testid="stAlertContainer"][class*="info"] {
    background: rgba(96,165,250,0.08) !important;
    border-left-color: #60a5fa !important;
}
[data-testid="stAlertContainer"][class*="success"] {
    background: rgba(52,211,153,0.08) !important;
    border-left-color: #34d399 !important;
}
[data-testid="stAlertContainer"][class*="warning"] {
    background: rgba(251,191,36,0.08) !important;
    border-left-color: #fbbf24 !important;
}
[data-testid="stAlertContainer"][class*="error"] {
    background: rgba(248,113,113,0.08) !important;
    border-left-color: #f87171 !important;
}

/* ===== SPINNER ===== */
.stSpinner > div { border-top-color: #a78bfa !important; }

/* ===== PROGRESS BAR ===== */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #60a5fa) !important;
    border-radius: 8px !important;
}
.stProgress > div > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.45), rgba(79,70,229,0.4)) !important;
    color: #e2e8f0 !important;
    box-shadow: 0 2px 8px rgba(124,58,237,0.25) !important;
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stDataFrame"] th {
    background: rgba(124,58,237,0.15) !important;
    color: #c4b5fd !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stDataFrame"] td {
    color: #e2e8f0 !important;
    background: rgba(255,255,255,0.02) !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}

/* ===== RADIO ===== */
.stRadio label, .stRadio p { color: #cbd5e1 !important; }
.stRadio > div { gap: 0.35rem !important; }
[data-baseweb="radio"] div { border-color: rgba(124,58,237,0.5) !important; }

/* ===== CHECKBOX ===== */
.stCheckbox label { color: #cbd5e1 !important; }

/* ===== HR ===== */
hr {
    border: none !important;
    border-top: 1px solid rgba(124,58,237,0.18) !important;
    margin: 1.2rem 0 !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.4); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,58,237,0.65); }

/* ===== COLUMN GAPS ===== */
[data-testid="stHorizontalBlock"] { gap: 1rem !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ============================================================
   CUSTOM COMPONENT CLASSES
   ============================================================ */

/* Premium Card */
.premium-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(124,58,237,0.18);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.2);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    height: 100%;
}
.premium-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 40px rgba(124,58,237,0.18);
    border-color: rgba(124,58,237,0.35);
}
.premium-card h3 { color: #e2e8f0 !important; font-size: 1.1rem !important; margin-bottom: 0.5rem !important; }
.premium-card p  { color: #94a3b8 !important; font-size: 0.88rem !important; line-height: 1.6 !important; }

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(79,70,229,0.12), rgba(52,211,153,0.07));
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 22px;
    padding: 2.5rem 2rem;
    text-align: center;
    backdrop-filter: blur(16px);
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, rgba(124,58,237,0.08) 0%, transparent 70%);
    animation: pulse-bg 6s ease-in-out infinite;
    pointer-events: none;
}
@keyframes pulse-bg {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.08); opacity: 0.7; }
}

/* Keyword Pill */
.kw-pill {
    display: inline-block;
    background: linear-gradient(135deg, rgba(124,58,237,0.28), rgba(79,70,229,0.2));
    border: 1px solid rgba(124,58,237,0.35);
    border-radius: 20px;
    padding: 0.28rem 0.8rem;
    margin: 0.2rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: #c4b5fd !important;
    backdrop-filter: blur(8px);
    transition: all 0.18s ease;
    cursor: default;
    white-space: nowrap;
}
.kw-pill:hover {
    background: linear-gradient(135deg, rgba(124,58,237,0.48), rgba(79,70,229,0.38));
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(124,58,237,0.25);
}

/* Score Badge */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1.2rem;
    border-radius: 30px;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.02em;
}
.badge-excellent {
    background: rgba(52,211,153,0.12);
    border: 1px solid rgba(52,211,153,0.4);
    color: #34d399 !important;
}
.badge-good {
    background: rgba(96,165,250,0.12);
    border: 1px solid rgba(96,165,250,0.4);
    color: #60a5fa !important;
}
.badge-review {
    background: rgba(251,146,60,0.12);
    border: 1px solid rgba(251,146,60,0.4);
    color: #fb923c !important;
}

/* Step Progress Item */
.step-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.55rem 1rem;
    border-radius: 10px;
    margin-bottom: 0.35rem;
    font-size: 0.88rem;
    color: #64748b !important;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.05);
}
.step-item.done {
    color: #34d399 !important;
    background: rgba(52,211,153,0.06);
    border-color: rgba(52,211,153,0.2);
}
.step-item.active {
    color: #a78bfa !important;
    background: rgba(124,58,237,0.1);
    border-color: rgba(124,58,237,0.3);
    animation: pulse-border 1.5s ease-in-out infinite;
}
@keyframes pulse-border {
    0%, 100% { border-color: rgba(124,58,237,0.3); }
    50% { border-color: rgba(124,58,237,0.7); }
}

/* Info strip */
.info-strip {
    background: rgba(96,165,250,0.08);
    border: 1px solid rgba(96,165,250,0.22);
    border-radius: 10px;
    padding: 0.65rem 1rem;
    color: #93c5fd !important;
    font-size: 0.87rem;
    margin-bottom: 0.8rem;
}

/* Flashcard face */
.flashcard-face {
    width: 100%;
    min-height: 240px;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 6px 28px rgba(0,0,0,0.2);
}
.flashcard-front {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(79,70,229,0.14));
    border: 1px solid rgba(124,58,237,0.32);
}
.flashcard-back {
    background: linear-gradient(135deg, rgba(52,211,153,0.14), rgba(16,185,129,0.09));
    border: 1px solid rgba(52,211,153,0.32);
}

/* Stat mini-card */
.stat-mini {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(124,58,237,0.18);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    text-align: center;
}
.stat-mini .stat-val {
    font-family: 'Outfit', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #a78bfa;
}
.stat-mini .stat-label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 2px;
}

/* Source box */
.source-box {
    background: rgba(255,255,255,0.03);
    border-left: 3px solid rgba(96,165,250,0.45);
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 0.9rem;
    margin: 0.35rem 0;
    font-size: 0.82rem;
    color: #94a3b8 !important;
    font-style: italic;
}

/* Confidence pill */
.conf-pill {
    display: inline-block;
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.22);
    border-radius: 10px;
    padding: 0.12rem 0.55rem;
    font-size: 0.72rem;
    color: #34d399 !important;
    font-weight: 600;
}

</style>
"""


def inject_css():
    """Inject the premium CSS. Use st.html if available to avoid Markdown parser mangling CSS."""
    if hasattr(st, "html"):
        st.html(PREMIUM_CSS)
    else:
        st.markdown(PREMIUM_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """Render a styled page header with optional subtitle."""
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(
            f"<p style='font-size:1rem; color:#94a3b8; margin-top:-8px; margin-bottom:1rem;'>"
            f"{subtitle}</p>",
            unsafe_allow_html=True
        )


def keyword_pills_html(keywords: list) -> str:
    """Convert a list of keywords into styled pill badges HTML."""
    if not keywords:
        return ""
    pills = "".join(f"<span class='kw-pill'>{kw}</span>" for kw in keywords if kw.strip())
    return f"<div style='margin: 0.5rem 0 1rem 0; line-height: 2.2;'>{pills}</div>"


def score_badge_html(score: int, total: int) -> str:
    """Return an HTML score badge based on percentage."""
    pct = (score / total * 100) if total > 0 else 0
    if pct >= 80:
        cls, icon, label = "badge-excellent", "🏆", "Excellent!"
    elif pct >= 60:
        cls, icon, label = "badge-good", "👍", "Good Work"
    else:
        cls, icon, label = "badge-review", "📖", "Keep Reviewing"
    return (
        f"<div class='score-badge {cls}'>"
        f"{icon} {score}/{total} — {label} ({pct:.0f}%)"
        f"</div>"
    )
