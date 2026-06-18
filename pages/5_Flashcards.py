import streamlit as st
import os
from database.database import get_all_lectures, get_flashcards, save_flashcards
from models.flashcard_generator import create_flashcards
from utils.styles import inject_css, page_header

inject_css()



page_header("📇 Flashcards", "Study key concepts with AI-generated question & answer cards.")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload a lecture first.")
    st.stop()

options = {lec['id']: lec['title'] for lec in lectures}
selected_id = st.selectbox(
    "Select Lecture",
    options=list(options.keys()),
    format_func=lambda x: options[x]
)

flashcards = get_flashcards(selected_id)

# ── No flashcards yet ─────────────────────────────────────────────────────
if not flashcards:
    st.info("No flashcards found for this lecture.")
    num_cards = st.slider("How many flashcards to generate?", 4, 15, 8)
    if st.button("✨ Generate Flashcards", use_container_width=False):
        text_path = os.path.join(
            os.path.dirname(__file__), '..', 'uploads', 'texts', f"{selected_id}.txt"
        )
        if os.path.exists(text_path):
            with st.spinner("Generating flashcards using AI…"):
                with open(text_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                new_fcs = create_flashcards(text, num_cards=num_cards)
                save_flashcards(selected_id, new_fcs)
            st.success(f"✅ {len(new_fcs)} flashcards generated!")
            st.rerun()
        else:
            st.error("Source text not found. Please re-upload the lecture.")
    st.stop()

# ── Session state init ────────────────────────────────────────────────────
if ('fc_lecture' not in st.session_state or
        st.session_state.fc_lecture != selected_id):
    st.session_state.fc_lecture    = selected_id
    st.session_state.fc_index      = 0
    st.session_state.fc_flipped    = False
    st.session_state.fc_known      = set()
    st.session_state.fc_review     = set()

idx        = st.session_state.fc_index
total      = len(flashcards)
current_fc = flashcards[idx]
known_set  = st.session_state.fc_known
review_set = st.session_state.fc_review

# ── Progress bar ──────────────────────────────────────────────────────────
answered = len(known_set) + len(review_set)
pct = int(answered / total * 100)
st.html(
    f"<div class='progress-meta'>"
    f"<span>Card <strong>{idx + 1}</strong> of {total}</span>"
    f"<span><span style='color:#34d399;'>✅ {len(known_set)} known</span> &nbsp; "
    f"<span style='color:#fb923c;'>🔁 {len(review_set)} review</span></span>"
    f"</div>"
    f"<div class='progress-track'><div class='progress-fill' style='width:{pct}%;'></div></div>"
)

# ── Flashcard display ─────────────────────────────────────────────────────
_, card_col, _ = st.columns([1, 7, 1])
with card_col:
    if not st.session_state.fc_flipped:
        # Front — Question
        st.html(f"""
        <div class='flashcard-face flashcard-front'>
            <div class='fc-label'>QUESTION</div>
            <div class='fc-text'>{current_fc['question']}</div>
        </div>
        <div class='muted-hint'>👇 Click "Reveal Answer" to flip the card</div>
        """)
    else:
        # Back — Answer
        st.html(f"""
        <div class='flashcard-face flashcard-back'>
            <div class='fc-label'>ANSWER</div>
            <div class='fc-text'>{current_fc['answer']}</div>
        </div>
        """)

st.write("")

# ── Flip button ───────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([2, 4, 2])
with btn_col:
    flip_label = "👁️ Reveal Answer" if not st.session_state.fc_flipped else "🔄 Back to Question"
    if st.button(flip_label, use_container_width=True):
        st.session_state.fc_flipped = not st.session_state.fc_flipped
        st.rerun()

# ── Self-assessment buttons (only visible after reveal) ───────────────────
if st.session_state.fc_flipped:
    st.write("")
    ka_col, ra_col = st.columns(2)
    with ka_col:
        if st.button("✅ I Know This", use_container_width=True,
                     help="Mark this card as learned"):
            known_set.add(idx)
            review_set.discard(idx)
            st.session_state.fc_known  = known_set
            st.session_state.fc_review = review_set
            # Auto-advance
            if idx < total - 1:
                st.session_state.fc_index   = idx + 1
                st.session_state.fc_flipped = False
            st.rerun()
    with ra_col:
        if st.button("🔁 Review Again", use_container_width=True,
                     help="Mark for further review"):
            review_set.add(idx)
            known_set.discard(idx)
            st.session_state.fc_known  = known_set
            st.session_state.fc_review = review_set
            if idx < total - 1:
                st.session_state.fc_index   = idx + 1
                st.session_state.fc_flipped = False
            st.rerun()

st.markdown("---")

# ── Navigation ────────────────────────────────────────────────────────────
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("⬅️ Previous", use_container_width=True, disabled=(idx == 0)):
        st.session_state.fc_index   = idx - 1
        st.session_state.fc_flipped = False
        st.rerun()
with nav2:
    if st.button("🔀 Shuffle", use_container_width=True):
        import random
        shuffled = list(range(total))
        random.shuffle(shuffled)
        # Persist shuffled order
        flashcards_shuffled = [flashcards[i] for i in shuffled]
        st.session_state.fc_index   = 0
        st.session_state.fc_flipped = False
        st.info("Cards shuffled! (Reload the page to apply)")
        st.rerun()
with nav3:
    if st.button("Next ➡️", use_container_width=True, disabled=(idx == total - 1)):
        st.session_state.fc_index   = idx + 1
        st.session_state.fc_flipped = False
        st.rerun()

st.write("")

# ── Regenerate button ─────────────────────────────────────────────────────
with st.expander("⚙️ Regenerate Flashcards"):
    num_new = st.slider("Number of cards", 4, 15, 8, key="fc_regen_n")
    if st.button("🔄 Regenerate", use_container_width=True, key="fc_regen_btn"):
        text_path = os.path.join(
            os.path.dirname(__file__), '..', 'uploads', 'texts', f"{selected_id}.txt"
        )
        if os.path.exists(text_path):
            with st.spinner("Re-generating flashcards…"):
                with open(text_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                new_fcs = create_flashcards(text, num_cards=num_new)
                save_flashcards(selected_id, new_fcs)
            st.success("Flashcards regenerated!")
            st.session_state.fc_index   = 0
            st.session_state.fc_flipped = False
            st.session_state.fc_known   = set()
            st.session_state.fc_review  = set()
            st.rerun()
