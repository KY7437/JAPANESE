import streamlit as st

st.set_page_config(page_title="Speech Comparison App", layout="wide")

st.title("🗣️ Pronunciation Analysis App")

st.markdown("""
왼쪽 사이드바에서 분석 도구를 선택하세요.

- **Soundwave** : 파형 비교  
- **Formants** : 포먼트(F1/F2) 비교
""")
