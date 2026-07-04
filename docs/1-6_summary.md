````markdown
# Lesson 1–6 Notes: Foundations of Retrieval-Augmented Generation (RAG)

---

# Overview

Before an AI can answer questions from documents, it must first understand those documents.

The first six lessons focused on building the **retrieval pipeline**, which is responsible for finding relevant information before an LLM generates an answer.

```text
PDF
 │
 ▼
Extract Text
 │
 ▼
Chunk Text
 │
 ▼
Generate Embeddings
 │
 ▼
Store Embeddings
 │
 ▼
Semantic Search
 │
 ▼
Relevant Chunks
```

---

# 1. What is RAG?

RAG stands for:

**Retrieval-Augmented Generation**

Instead of asking an LLM to answer from memory, we first retrieve relevant information and then provide that information to the LLM.

```text
User Question
      │
      ▼
Retrieve Relevant Information
      │
      ▼
Provide Context to LLM
      │
      ▼
Generate Answer
```

Benefits:

- More accurate answers
- Answers based on documents
- Reduced hallucinations
- Can work with private documents

---

# 2. Project Pipeline

The overall workflow of our AI Research Assistant is:

```text
PDF

↓

Extract Text

↓

Chunk Text

↓

Generate Embeddings

↓

Semantic Search

↓

Prompt Construction

↓

LLM

↓

Answer
```

We built this pipeline step by step instead of using existing frameworks.

---

# 3. PDF Text Extraction

The first task is extracting text from PDFs.

Example:

```python
text = extract_text("document.pdf")
```

Problem:

Some PDFs contain real text.

Others only contain images.

Example:

```text
PDF

↓

Scanned Image

↓

No Text Found
```

For image-based PDFs, OCR is required.

---

# 4. OCR (Optical Character Recognition)

OCR converts images into text.

Workflow:

```text
PDF Page

↓

Image

↓

OCR

↓

Extracted Text
```

OCR is necessary for:

- Scanned books
- Handwritten notes (to some extent)
- Image-based PDFs

Without OCR, image-only PDFs return little or no text.

---

# 5. Why Chunk Documents?

Large documents cannot be embedded as a single piece.

Example:

```text
500 Pages

↓

One Embedding
```

This loses important information.

Instead:

```text
500 Pages

↓

Chunk 1

Chunk 2

Chunk 3

...

Chunk N
```

Each chunk receives its own embedding.

---

# 6. Chunking Strategies

Initially we split text by a fixed number of words.

Example:

```python
def chunk_text(text, chunk_size=100, overlap=20):
    ...
```

Problem:

A sentence may be split into two chunks.

Example:

```
Machine Learning is a subset

of Artificial Intelligence.
```

The AI receives incomplete information.

---

## Better Strategy

Split by **sentences**.

Example:

```text
Sentence 1

Sentence 2

Sentence 3
```

Advantages:

- Preserves meaning
- Better retrieval
- Better answers
- More natural context

---

# 7. Why Overlap?

Suppose two consecutive chunks are:

```text
Chunk 1

Machine Learning is a subset...
```

```text
Chunk 2

...of Artificial Intelligence.
```

Without overlap:

Important information may be separated.

With overlap:

```text
Chunk 1

Sentence A

Sentence B

Sentence C
```

```text
Chunk 2

Sentence C

Sentence D

Sentence E
```

The shared sentence preserves context.

---

# 8. Embeddings

An embedding converts text into numbers.

Example:

```text
Machine Learning

↓

[-0.12, 0.58, ...]
```

The vector captures the semantic meaning of the text.

Computers compare vectors instead of comparing words.

---

# 9. Sentence Transformers

We used:

```
sentence-transformers/all-MiniLM-L6-v2
```

Example:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

embedding = model.encode(text)
```

Output:

```text
Shape

↓

(384,)
```

Every sentence becomes a **384-dimensional vector**.

---

# 10. Semantic Similarity

Two sentences with similar meanings produce similar embeddings.

Example:

```
I love dogs.

I like puppies.
```

High similarity.

Another example:

```
Artificial Intelligence

The weather is sunny.
```

Low similarity.

Embeddings capture meaning rather than exact words.

---

# 11. Cosine Similarity

Cosine similarity measures how similar two vectors are.

Formula:

```
A · B
-----------
||A|| ||B||
```

Interpretation:

```
1.0

↓

Very Similar
```

```
0

↓

Unrelated
```

```
-1

↓

Opposite Direction
```

Most sentence embeddings produce values between **0 and 1**.

---

# 12. Dot Product

Dot Product:

```
A · B

=

Σ(x × y)
```

Used as part of cosine similarity.

We first implemented it manually before using NumPy.

---

# 13. Semantic Search

Workflow:

```text
Documents

↓

Generate Embeddings

↓

Store Embeddings

↓

User Question

↓

Generate Query Embedding

↓

Cosine Similarity

↓

Sort Results

↓

Return Top K
```

This allows us to retrieve information based on meaning instead of exact words.

---

# 14. Building a Document Store

Initially we stored:

```python
document_store = [
    {
        "text": "...",
        "embedding": ...
    }
]
```

This allowed us to:

- Store document text
- Store embeddings
- Perform semantic search

---

# 15. Semantic Search Algorithm

Algorithm:

```text
Generate Query Embedding

↓

Compare with Every Document

↓

Calculate Cosine Similarity

↓

Sort

↓

Return Top Results
```

Pseudo-code:

```python
for document in documents:

    similarity = cosine_similarity(
        query_embedding,
        document_embedding
    )

sort()

return top_k
```

---

# 16. Prompt Construction

The retrieval system does not answer questions.

It only returns the most relevant chunks.

Those chunks are later used to build the prompt.

Example:

```text
Context

[Relevant Chunk 1]

[Relevant Chunk 2]

Question

What is Machine Learning?
```

---

# 17. Project Structure

By Lesson 6, the project structure looked like:

```text
backend/

├── app.py
│
├── data/
│
├── embeddings/
│   ├── model.py
│   ├── embedding_demo.py
│   └── vector_math.py
│
├── retrieval/
│   ├── semantic_search.py
│   └── document_store.py
│
└── prompts/
```

Later lessons refactored this structure into a more scalable architecture.

---

# Key Concepts Learned

- Retrieval-Augmented Generation (RAG)
- PDF text extraction
- OCR
- Document chunking
- Sentence-based chunking
- Chunk overlap
- Embeddings
- Sentence Transformers
- Dot Product
- Cosine Similarity
- Semantic Search
- Prompt Construction

---

# Key Takeaways

- AI cannot search documents without embeddings.
- Chunk quality directly affects answer quality.
- Sentence-based chunking is better than fixed-word chunking.
- Embeddings represent meaning, not keywords.
- Semantic search retrieves information based on similarity.
- Retrieval happens **before** the LLM generates an answer.
- Understanding each step manually makes it easier to build and debug production RAG systems.

---

# Completed Milestones

- ✅ PDF Processing
- ✅ OCR Integration
- ✅ Sentence-Based Chunking
- ✅ Embedding Generation
- ✅ Cosine Similarity
- ✅ Semantic Search
- ✅ Prompt Construction (Initial Version)

---

# Next Topics (Lessons 7–15)

- Large Language Models (LLMs)
- Ollama
- Local Inference
- Prompt Engineering
- Embedding Service
- Dependency Injection
- FAISS
- DocumentStore
- SearchResult Data Class
- Clean Architecture
````
