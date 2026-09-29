from sentence_transformers import SentenceTransformer
import chromadb
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
with open("ai_sample.txt", "r") as file:
    text = file.read()
#print(text)
#print("No of characters: ", len(text))
chunks = []
chunk_size = 25 #20, 30, 50
chunk_overlap = 10 #5, 15, 30
step = chunk_size - chunk_overlap
for i in range(0, len(text), chunk_size):
    chunk = text[i:i+chunk_size]
    chunks.append(chunk)
# print("No of chunks:", len(chunks))
# for i in range(len(chunks)):
#     print(f"chunk {i} -> {chunks[i]}")
#Embeddings
embeddings = model.encode(chunks)
# print("Embeddings created successfully.")
# print("No of embeddings:",len(embeddings))
# print(embeddings[0])
print(embeddings.shape)

# chroma db
client = chromadb.Client()
collection = client.create_collection(name="My_documents")
print("Collection created successfully.")
ids = []
for i in range(len(chunks)):
    ids.append(str(i))
collection.add(
    ids = ids,
    documents=chunks,
    embeddings=embeddings.tolist()
)
print("No of item in the collection: ", collection.count())
results = collection.get()
for i in range(len(results["ids"])):
     print(f"ID: {results['ids'][i]} -> chunk: {results['documents'][i]}")