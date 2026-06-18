import streamlit as st
from database.database import get_all_lectures, get_notes

st.title("📝 Notes Viewer")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found.")
else:
    options = {lec['id']: lec['title'] for lec in lectures}
    selected_id = st.selectbox("Select a lecture to view notes", options=list(options.keys()), format_func=lambda x: options[x])
    
    notes = get_notes(selected_id)
    
    if not notes:
        st.info("No notes generated for this lecture yet. Please go to 'Notes Generator'.")
    else:
        st.markdown("### Executive Summary")
        st.write(notes['summary'])
        
        st.markdown("### Key Concepts")
        # Assuming keywords are comma-separated
        keywords_list = [k.strip() for k in notes['keywords'].split(',')]
        
        cols = st.columns(4)
        for i, kw in enumerate(keywords_list):
            if kw:
                cols[i % 4].markdown(f"**{kw}**")
                
        # Export functionality placeholder
        st.markdown("---")
        if st.button("Export to PDF (Coming Soon)"):
            st.info("PDF Export will be available in the next update!")
