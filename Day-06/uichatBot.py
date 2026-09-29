import ollama
import streamlit as st
st.title(":red[welcome to my ChatBot App!!!]")
with st.sidebar:
    st.header(":blue[Chat Settings]")
    if st.button("clear chat🗑️ "):
        st.session_state.messages=[]
        st.success("Chat cleared")
    personalities = {
    "Friend ": "Answer the questions in a friendly and casual manner. Give answers in two lines.",
    "Teacher": "Answer the questions in a simple and educational manner.",
    "Professional": "Answer the questions in a professional and clear manner."
}
    personality = st.sidebar.selectbox(
    "Select a personality",
    personalities.keys()
)
    uploaded_file = st.file_uploader("upload a file...")
    try:
        if uploaded_file:
            context=uploaded_file.read().decode("utf-8")
            st.success("file uploaded successfully")
            if st.button("Display"):
                st.text(context)
    except:
        st.error("invalid file")
if "messages"not in st.session_state:
    st.session_state.messages=[]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
question=st.chat_input("you:")
if question:
    st.session_state.messages.append(
        {"role":"user",
        "content":question}
        )
    with st.chat_message("user"):
        st.write(question)
    with st.spinner("Thinking..."):
        response=ollama.chat(
            model="llama3.2:3b",
            messages=[
               {"role":"system","content":personalities[personality]}]
                + st.session_state.messages)
    st.session_state.messages.append(
        {
        "role":"assistant",
        "content":response["message"]["content"]}
        )
    with st.chat_message("assistant"):
        st.write(response["message"]["content"])
