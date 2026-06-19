import streamlit as st
from database.database import get_all_lectures
from models.rag_engine import query_rag
from utils.styles import inject_css, page_header

inject_css()
page_header("🤖 AI Study Assistant",
            "Ask any question — the AI searches your lecture and synthesises a precise answer.")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload one first.")
    st.stop()

options = {lec['id']: lec['title'] for lec in lectures}

# ── Sidebar-like controls in main area ───────────────────────────────────
ctrl1, ctrl2 = st.columns([4, 1])
with ctrl1:
    selected_id = st.selectbox(
        "Lecture Context",
        options=list(options.keys()),
        format_func=lambda x: options[x]
    )
with ctrl2:
    st.write("")
    st.write("")
    if st.button("🗑️ Clear Chat", use_container_width=True, help="Clear conversation history"):
        if selected_id in st.session_state.get('messages', {}):
            del st.session_state.messages[selected_id]
        st.rerun()

st.markdown("---")

# ── Chat history init ─────────────────────────────────────────────────────
if 'messages' not in st.session_state:
    st.session_state.messages = {}

if selected_id not in st.session_state.messages:
    st.session_state.messages[selected_id] = [
        {
            "role":    "assistant",
            "content": (
                f"👋 Hi! I'm your AI Study Assistant for **'{options[selected_id]}'**.\n\n"
                "I can answer questions, explain concepts, and find specific information "
                "from your lecture. What would you like to know?"
            ),
        }
    ]

# ── Suggested starter questions ───────────────────────────────────────────
# Only show if no user messages exist yet
has_user_msgs = any(m['role'] == 'user' for m in st.session_state.messages[selected_id])

if not has_user_msgs:
    starter_qs = [
        "Summarise the main topics covered.",
        "What are the key definitions?",
        "Explain the most important concept.",
        "What are the practical applications?",
        "What should I focus on for an exam?",
    ]
    st.markdown("**💡 Try asking:**")
    chip_cols = st.columns(len(starter_qs))
    for col, q in zip(chip_cols, starter_qs):
        with col:
            if st.button(q, key=f"chip_{q}", use_container_width=True,
                         help=f"Click to ask: {q}"):
                st.session_state.messages[selected_id].append({"role": "user", "content": q})
                with st.spinner("Searching knowledge base…"):
                    resp = query_rag(selected_id, q)
                st.session_state.messages[selected_id].append({"role": "assistant", "content": resp})
                st.rerun()

st.write("")

# ── Message display ───────────────────────────────────────────────────────
for msg in st.session_state.messages[selected_id]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask anything about the lecture…"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages[selected_id].append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching knowledge base and generating answer…"):
            response = query_rag(selected_id, prompt)
        st.markdown(response, unsafe_allow_html=True)
    st.session_state.messages[selected_id].append({"role": "assistant", "content": response})

# ── Session stats ─────────────────────────────────────────────────────────
msg_list = st.session_state.messages.get(selected_id, [])
user_msgs = [m for m in msg_list if m['role'] == 'user']
if user_msgs:
    st.html(
        f"<small style='color:#475569;'>{len(user_msgs)} question(s) asked this session</small>"
    )
