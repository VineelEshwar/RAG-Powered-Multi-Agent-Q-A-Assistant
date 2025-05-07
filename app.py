

import streamlit as st
from agent import agent

st.set_page_config(page_title="🧠 RAG + Agent Q&A Assistant", layout="centered")

st.title("🧠 RAG-Powered Multi-Agent Q&A Assistant")
st.markdown("Ask anything — the agent will decide whether to use RAG, calculator, dictionary, or Wikipedia.")

user_input = st.text_input("Enter your question:")
if st.button("Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            response = agent.run(user_input)
            st.markdown("### 🧠 Answer:")
            st.write(response)