import streamlit as st
st.title("My first streamlist App!!!")
st.write("Welcome to my AI application!")
name = st.text_input("Enter your name: ")
if st.button("Submit"):
    st.write("Hello", name) 
