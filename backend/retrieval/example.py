import faiss
import numpy as np

dimension = 384

index = faiss.IndexFlatIP(dimension)

vectors = np.random.rand(3, 384).astype("float32")

print(index)

faiss.normalize_L2(vectors)
index.add(vectors)

print(index.ntotal)

query = np.random.rand(1, dimension).astype("float32")

faiss.normalize_L2(query)

distances, indices = index.search(query, k=2)

print(distances)
print(indices)