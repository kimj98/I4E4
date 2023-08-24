import streamlit as st

def home_menu():
    st.title("유사특허")
    user_input = st.text_input("유사특허", "특허 내용 입력란")
    
