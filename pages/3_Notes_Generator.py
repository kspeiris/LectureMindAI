import streamlit as st
import os
from database.database import get_all_lectures, save_notes, get_notes
from models.summarizer import generate_summary
from models.keyword_extractor import extract_keywords
from models.rag_engine import build_faiss_index

st.title("⚙️ Notes Generator")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload a lecture first.")
else:
    options = {lec['id']: lec['title'] for lec in lectures}
    selected_id = st.selectbox("Select a lecture to generate notes", options=list(options.keys()), format_func=lambda x: options[x])
    
    existing_notes = get_notes(selected_id)
    if existing_notes:
        st.info("Notes already exist for this lecture. Generating again will overwrite them.")
        
    if st.button("Generate Smart Notes & Index for AI Assistant"):
        with st.spinner("Loading AI Models and processing (this may take a few minutes)..."):
            try:
                # Load text
                text_path = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'texts', f"{selected_id}.txt")
                with open(text_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    
                st.text("Step 1/3: Generating Summary...")
                summary = generate_summary(text)
                
                st.text("Step 2/3: Extracting Keywords...")
                keywords = extract_keywords(text)
                
                st.text("Step 3/3: Building Knowledge Base for AI Assistant...")
                build_faiss_index(selected_id, text)
                
                save_notes(selected_id, summary, keywords)
                
                st.success("Notes generated successfully! You can view them in the Notes Viewer.")
            except Exception as e:
                st.error(f"Error during generation: {str(e)}")
