def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size")
    if overlap < 0:
        raise ValueError("Overlap must be non-negative")
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")


    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)

    return chunks


sample_text = """
Artificial Intelligence is changing the world by automating complex tasks.
Machine Learning is a subset of Artificial Intelligence.
Deep Learning uses neural networks.
Large Language Models can generate human-like text.
"""

chunks = chunk_text(sample_text, chunk_size=8, overlap=8)

for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i}:")
    print(chunk)
    print("-" * 50)
