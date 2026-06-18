import streamlit as st
import os
from services.pdf_processor import extract_text_from_pdf
from services.ppt_processor import extract_text_from_ppt
from database.database import add_lecture

st.title("📤 Upload Lecture")
st.markdown("Upload your lecture materials (PDF or PPTX) to start generating intelligent study aids.")

# Ensure upload directory exists
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(os.path.join(UPLOAD_DIR, 'pdfs'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'pptx'), exist_ok=True)

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "pptx"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file_ext + "s", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.success(f"File {uploaded_file.name} uploaded successfully!")
    
    if st.button("Process Document"):
        with st.spinner("Extracting text and analyzing document..."):
            try:
                if file_ext == "pdf":
                    data = extract_text_from_pdf(file_path)
                elif file_ext == "pptx":
                    data = extract_text_from_ppt(file_path)
                    
                # Save to database
                lecture_id = add_lecture(
                    title=uploaded_file.name,
                    filename=uploaded_file.name,
                    pages=data['pages'],
                    word_count=data['word_count']
                )
                
                # Save the raw text for later use in generation
                text_dir = os.path.join(UPLOAD_DIR, 'texts')
                os.makedirs(text_dir, exist_ok=True)
                with open(os.path.join(text_dir, f"{lecture_id}.txt"), 'w', encoding='utf-8') as f:
                    f.write(data['text'])
                    
                st.success(f"Document processed! Extracted {data['pages']} pages and {data['word_count']} words.")
                st.info("You can now go to Notes Generator to create summaries, or AI Assistant to chat with the document.")
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
