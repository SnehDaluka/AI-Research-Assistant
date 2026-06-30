from model import model
from backend.data.documents import documents

# sentences = [
#     "I love dogs.",
#     "I like puppies.",
#     "Artificial Intelligence is amazing.",
#     "The weather is sunny today.",
#     "I hate dogs"
# ]

sentences = [
    "Apple",
    "Apple Inc.",
    "Apple fruit",
    "Microsoft",
    "Banana"
]


embeddings = model.encode(documents)

# for i, embedding in enumerate(embeddings):
#     print(f"Sentence: {sentences[i]}")
#     print(f"Shape: {embedding.shape}")
#     print(f"First 10 values: {embedding[:10]}...")
#     print("-" * 50)
    
# from sklearn.metrics.pairwise import cosine_similarity

# similarity = cosine_similarity(embeddings)

# from vector_math import cosine_similarity

# similarity = cosine_similarity(
#     embeddings[0],
#     embeddings[1]
# )
# print(similarity)

