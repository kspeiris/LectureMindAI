import streamlit as st

st.set_page_config(
    page_title='LectureMind AI',
    page_icon='📚',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS for Dark/Light Mode + Premium feel
def apply_theme(theme_name):
    if theme_name == 'Dark':
        css = """
        <style>
        .stApp {
            background-color: #121212;
            color: #ffffff;
        }
        .stMetric {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        </style>
        """
    else:
        css = """
        <style>
        .stApp {
            background-color: #f8f9fa;
            color: #212529;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

with st.sidebar:
    st.title('📚 LectureMind AI')
    st.markdown("---")
    selected_theme = st.selectbox('Theme', ['Light', 'Dark'], index=0 if st.session_state.theme == 'Light' else 1)
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

apply_theme(st.session_state.theme)

st.title('LectureMind AI Educational Assistant')
st.markdown("""
Welcome to **LectureMind AI**, your personal AI-powered study assistant.

Use the sidebar to navigate to different modules:
- 📊 **Dashboard:** View your overall learning progress.
- 📤 **Upload Lecture:** Add new PDFs or PPTs to generate study materials.
- 📝 **Notes Viewer:** Read auto-generated summaries and keywords.
- 📇 **Flashcards:** Revise using interactive flashcards.
- ✍️ **MCQ Quiz:** Test your knowledge.
- 🤖 **AI Study Assistant:** Ask contextual questions based on your lecture.
""")
