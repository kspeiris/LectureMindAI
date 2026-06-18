import streamlit as st
from database.database import get_all_lectures
from models.rag_engine import query_rag

st.title("🤖 AI Study Assistant")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload one first.")
else:
    options = {lec['id']: lec['title'] for lec in lectures}
    selected_id = st.selectbox("Select Lecture Context", options=list(options.keys()), format_func=lambda x: options[x])
    
    st.markdown("---")
    
    # Initialize chat history for this lecture
    if 'messages' not in st.session_state:
        st.session_state.messages = {}
        
    if selected_id not in st.session_state.messages:
        st.session_state.messages[selected_id] = [
            {"role": "assistant", "content": f"Hi! I'm your AI Study Assistant. Ask me anything about '{options[selected_id]}'!"}
        ]
        
    # Display chat messages
    for msg in st.session_state.messages[selected_id]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Chat input
    if prompt := st.chat_input("Ask a question based on the lecture..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to history
        st.session_state.messages[selected_id].append({"role": "user", "content": prompt})
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                response = query_rag(selected_id, prompt)
                st.markdown(response)
        # Add bot message to history
        st.session_state.messages[selected_id].append({"role": "assistant", "content": response})
