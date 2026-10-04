from sentence_transformers import util, SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
Sentences = [
    "I love playing football",
    "I enjoy playing soccere",
    "I like eating pizza",
]
Sentence_embedding = model.encode(Sentences)
similarity = util.cos_sim(Sentence_embedding[0], Sentence_embedding[1])
similarity = util.cos_sim(Sentence_embedding[1], Sentence_embedding[2])
similarity = util.cos_sim(Sentence_embedding[0], Sentence_embedding[2])
print(similarity.item())