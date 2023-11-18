import streamlit as st
import numpy as np


with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))

prompt = st.chat_input("Say something")
if prompt:
    st.write(prompt)