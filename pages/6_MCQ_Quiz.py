import streamlit as st
import os
from database.database import get_all_lectures, get_mcqs, save_mcqs, save_quiz_result
from models.mcq_generator import generate_mcqs

st.title("✍️ MCQ Quiz")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found.")
else:
    options = {lec['id']: lec['title'] for lec in lectures}
    selected_id = st.selectbox("Select Lecture for Quiz", options=list(options.keys()), format_func=lambda x: options[x])
    
    mcqs = get_mcqs(selected_id)
    
    if not mcqs:
        st.info("No MCQs found for this lecture.")
        if st.button("Generate MCQs"):
            with st.spinner("Generating multiple-choice questions using AI..."):
                text_path = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'texts', f"{selected_id}.txt")
                if os.path.exists(text_path):
                    with open(text_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    new_mcqs = generate_mcqs(text, num_mcqs=5)
                    save_mcqs(selected_id, new_mcqs)
                    st.success("MCQs generated!")
                    st.rerun()
                else:
                    st.error("Text data not found. Please re-upload the lecture.")
    else:
        st.markdown("### Test Your Knowledge")
        
        with st.form("quiz_form"):
            user_answers = {}
            for i, mcq in enumerate(mcqs):
                st.markdown(f"**Q{i+1}: {mcq['question']}**")
                # Prepare options
                options_list = [mcq['option_a'], mcq['option_b'], mcq['option_c'], mcq['option_d']]
                # Remove empty options
                options_list = [opt for opt in options_list if opt]
                
                user_answers[i] = st.radio(f"Select answer for Q{i+1}", options=options_list, key=f"q_{i}", label_visibility="collapsed")
                st.write("")
                
            submitted = st.form_submit_button("Submit Quiz")
            
            if submitted:
                score = 0
                for i, mcq in enumerate(mcqs):
                    if user_answers[i] == mcq['correct_answer']:
                        score += 1
                        
                st.success(f"You scored {score} out of {len(mcqs)}!")
                save_quiz_result(selected_id, score, len(mcqs))
                
                # Show correct answers
                with st.expander("Review Answers"):
                    for i, mcq in enumerate(mcqs):
                        st.markdown(f"**Q{i+1}: {mcq['question']}**")
                        if user_answers[i] == mcq['correct_answer']:
                            st.markdown(f"✅ Your answer: {user_answers[i]}")
                        else:
                            st.markdown(f"❌ Your answer: {user_answers[i]}")
                            st.markdown(f"✔️ Correct answer: {mcq['correct_answer']}")
                        st.markdown("---")
