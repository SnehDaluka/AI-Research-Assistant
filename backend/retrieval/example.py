import faiss
import numpy as np

dimension = 384

index = faiss.IndexFlatIP(dimension)

vectors = np.random.rand(3, 384).astype("float32")

print(index)

faiss.normalize_L2(vectors)
index.add(vectors)

print(index.ntotal)