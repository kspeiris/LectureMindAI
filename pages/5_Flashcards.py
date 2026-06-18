import streamlit as st
import os
from database.database import get_all_lectures, get_flashcards, save_flashcards
from models.flashcard_generator import create_flashcards

st.title("📇 Flashcards")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found.")
else:
    options = {lec['id']: lec['title'] for lec in lectures}
    selected_id = st.selectbox("Select Lecture", options=list(options.keys()), format_func=lambda x: options[x])
    
    flashcards = get_flashcards(selected_id)
    
    if not flashcards:
        st.info("No flashcards found for this lecture.")
        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards using AI..."):
                text_path = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'texts', f"{selected_id}.txt")
                if os.path.exists(text_path):
                    with open(text_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    new_fcs = create_flashcards(text, num_cards=5)
                    save_flashcards(selected_id, new_fcs)
                    st.success("Flashcards generated!")
                    st.rerun()
                else:
                    st.error("Text data not found. Please re-upload the lecture.")
    else:
        # Display Flashcards using a custom interactive UI pattern
        if 'fc_index' not in st.session_state:
            st.session_state.fc_index = 0
            st.session_state.show_answer = False
            
        current_fc = flashcards[st.session_state.fc_index]
        
        st.markdown(f"### Card {st.session_state.fc_index + 1} of {len(flashcards)}")
        
        card_col1, card_col2, card_col3 = st.columns([1, 6, 1])
        
        with card_col2:
            card_container = st.container(border=True)
            with card_container:
                st.markdown("<h4 style='text-align: center; color: #4A90E2;'>Question</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-size: 1.2em;'>{current_fc['question']}</p>", unsafe_allow_html=True)
                
                st.markdown("---")
                if st.session_state.show_answer:
                    st.markdown("<h4 style='text-align: center; color: #50E3C2;'>Answer</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-size: 1.1em;'>{current_fc['answer']}</p>", unsafe_allow_html=True)
                
                st.write("") # spacing
                if st.button("Flip Card" if not st.session_state.show_answer else "Hide Answer", use_container_width=True):
                    st.session_state.show_answer = not st.session_state.show_answer
                    st.rerun()
                    
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.fc_index = max(0, st.session_state.fc_index - 1)
                st.session_state.show_answer = False
                st.rerun()
        with col3:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.fc_index = min(len(flashcards) - 1, st.session_state.fc_index + 1)
                st.session_state.show_answer = False
                st.rerun()
