import ollama
import streamlit as st

# Title
st.title(":red[Welcome to my ChatBot App!!!]")

# File upload in sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload a text file...", type=["txt"])

    context = ""

    if uploaded_file:
        st.write("Uploaded file:", uploaded_file.name)
        context = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", context, height=200)

# Create message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
question = st.chat_input("You:")

if question:

    # Display user question
    with st.chat_message("user"):
        st.write(question)

    # Add user question to message history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Create prompt with uploaded file context
    if context:
        prompt = f"""
Use the following uploaded file content to answer the user's question.

File Content:
{context}

User Question:
{question}
"""
    else:
        prompt = question

    # Ask Ollama
    with st.spinner("Thinking..."):
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    # Get AI response
    answer = response["message"]["content"]

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Display AI response
    with st.chat_message("assistant"):
        st.write(answer)

