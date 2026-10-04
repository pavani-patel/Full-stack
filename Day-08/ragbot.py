from sentence_transformers import SentenceTransformer
import chromadb, ollama, streamlit as st
model = SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")
model = load_model()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="My_Documents")
st.snow()
st.title("My AI Chatbot!!")
with st.sidebar:
    st.header(":blue[Chat Settings⚙️]")
    if st.button("chat History"):
         for msg in st.session_state.messages:
              with st.chat_message(msg["role"]):
                   st.write(msg["content"])
    if st.button("Clear Chat🗑️"):
        st.session_state.messages = []
        st.success("Chat cleared👍")
    personalities = {
        "kid👶" : "Answer the question like you are responding to a 5 year old kid. Give the answer in 2 lines only",
        "Friend🤝" : "Answer the question in a friendly and casual manner. Give me the answer in 2 lines only",
        "Chef 🧑‍🍳" : "Answer the question. Give me the answer in 2 lines only"
    }
    personality = st.selectbox("Select a personality", personalities.keys())
    st.markdown("### 📁 File Upload")
    uploaded_file = st.file_uploader("📤 Upload a file....")
    if uploaded_file:
        file_name = uploaded_file.name
        text = uploaded_file.read().decode("utf-8", errors="ignore")
        with st.expander("Preview:"):
            st.text(text)

        chunks = []
        chunk_size = 100
        chunk_overlap = 20
        step = chunk_size - chunk_overlap
        for i in range(0, len(text), step):
            chunk = text[i:i + chunk_size] 
            chunks.append(chunk)     
        embeddings = model.encode(chunks)

        
        ids = []
        for i in range(len(chunks)):
            ids.append(f"{file_name}_{i}")
        collection.add(
            ids = ids,
            documents = chunks,
            embeddings = embeddings.tolist()
        )

#Query Phase
if "messages" not in st.session_state:
    st.session_state.messages = []

question = st.chat_input("Ask me a question......")
if question:
    if uploaded_file:
        with st.chat_message("user"):
            st.write(question)
        question_embedding = model.encode(question)
        results = collection.query(
            query_embeddings = [question_embedding.tolist()],
            n_results=3
        )
        retrived_results = results['documents'][0]
        retrived_ids = results['ids'][0]

        #Prompting
        context = '\n'.join(retrived_results)

        prompt = f"""
        Answerr the question using the context provided below.
        Question: {question}
        Context: {context}
        Answer:
        """

        #Connecting to Local Model
        response = ollama.chat(
            model="llama3.2:3b", 
            messages=[{
                "role": "user", 
                "content": prompt
            }]
        )
        answer = response['message']['content']

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
    else:
        st.session_state.messages.append({
                    "role": "assistant",
                    "content": question}
                    )
        with st.chat_message("user"):
                st.write(question)
        with st.spinner("Thinking...💭"):
                    response = ollama.chat(
                        model="llama3.2.:3b",
                        messages= [
                            {"role" : "system", "content": personalities[personality]}] + st.session_state.messages)
        st.session_state.messages.append(
                {"role": "assistant",
                "content": response["message"]["content"]}
            )
        with st.chat_message("assistant"):
            st.write("AI:", response["message"]["content"])