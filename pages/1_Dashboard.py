import streamlit as st
import pandas as pd
import plotly.express as px
from database.database import get_lecture_count, get_flashcards_count, get_mcq_count

st.title('📊 Learning Dashboard')
st.markdown("---")

lec_count = get_lecture_count()
fc_count = get_flashcards_count()
mcq_count = get_mcq_count()

c1, c2, c3, c4 = st.columns(4)
c1.metric('📚 Lectures Uploaded', lec_count)
c2.metric('📝 Notes Generated', lec_count) # 1 note per lecture
c3.metric('✍️ MCQs Created', mcq_count)
c4.metric('📇 Flashcards Generated', fc_count)

st.markdown("### Resources Overview")
df = pd.DataFrame({
    'Module': ['Lectures', 'Notes', 'MCQs', 'Flashcards'],
    'Count': [lec_count, lec_count, mcq_count, fc_count]
})

fig = px.bar(df, x='Module', y='Count', color='Module', title="Generated Content Distribution")
st.plotly_chart(fig, use_container_width=True)
