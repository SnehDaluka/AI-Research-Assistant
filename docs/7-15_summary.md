# Lesson 7–15 Notes: Building a Production-Style RAG Pipeline

---

# Overview

At this stage, our AI Research Assistant consists of several independent modules, each with a single responsibility.

```text
                User
                  │
                  ▼
          User Question
                  │
                  ▼
        Embedding Service
                  │
                  ▼
          Document Store
             (FAISS)
                  │
                  ▼
         Relevant Documents
                  │
                  ▼
          Prompt Builder
                  │
                  ▼
            LLM Generator
                  │
                  ▼
            Ollama Client
                  │
                  ▼
             Qwen 2.5 3B
                  │
                  ▼
              Final Answer
```

---

# 1. Large Language Models (LLMs)

An LLM is **not a search engine**.

Its job is to:

- Understand language
- Read context
- Generate natural language

It **does not retrieve information** from our documents.

Instead, we provide the relevant context.

## LLM Workflow

```text
Prompt
   │
   ▼
Tokenizer
   │
   ▼
Token IDs
   │
   ▼
Transformer
   │
   ▼
Next Token Prediction
   │
   ▼
Generated Answer
```

## What is a Token?

A token is **not always a word**.

Example:

```text
Machine Learning

↓

Machine
Learning
```

Another example:

```text
unbelievable

↓

un
believ
able
```

Programming code is also tokenized.

## Context Window

Every model has a maximum number of tokens it can process.

```
System Prompt
+
Retrieved Context
+
Question
+
Conversation History
=
Context Window
```

This is why chunking and retrieval are important.

---

# 2. Ollama

Ollama allows us to run language models locally.

Advantages:

- Free after download
- Private
- Offline support
- No API costs

Architecture:

```text
Python
   │
   ▼
Ollama Server
   │
   ▼
Local LLM
```

---

# 3. Prompt Construction

The prompt consists of:

```text
System Prompt
+
Retrieved Context
+
User Question
```

Example:

```text
Context

[1]
Machine Learning is a subset of Artificial Intelligence.

[2]
TensorFlow is a deep learning framework.

Question

What is Machine Learning?
```

## System Prompt

```text
You are an AI Research Assistant.

Answer ONLY using the provided context.

If the answer cannot be found,
respond with:

"I don't have enough information."
```

---

# 4. Embedding Model vs LLM

Our application uses **two different AI models**.

## Embedding Model

```
SentenceTransformer

↓

Text

↓

Embedding Vector
```

Example:

```
"What is AI?"

↓

[-0.24, 0.52, ...]
```

Used for:

- Semantic Search

---

## LLM

```
Prompt

↓

Answer
```

Used for:

- Natural language generation

---

# 5. Embedding Service

Instead of calling:

```python
model.encode(...)
```

everywhere,

we created:

```python
EmbeddingService
```

Responsibilities:

- Generate query embeddings
- Generate document embeddings
- Normalize embeddings
- Return embedding dimension

Example:

```python
query_embedding = embedding_service.embed_query(query)

document_embeddings = embedding_service.embed_documents(documents)
```

Benefits:

- Single place to change embedding models
- Cleaner architecture
- Easier maintenance

---

# 6. Separation of Responsibilities

## EmbeddingService

Responsible for:

- Generate embeddings
- Normalize embeddings
- Return embedding dimension

---

## DocumentStore

Responsible for:

- Store documents
- Store vectors
- Search vectors
- Return search results

---

## Prompt Builder

Responsible for:

- Build prompts

---

## LLM Generator

Responsible for:

- Generate answers

Every module has **one responsibility**.

---

# 7. Dependency Injection

Instead of:

```python
class DocumentStore:

    def __init__(self):
        self.embedding_service = EmbeddingService()
```

We use:

```python
embedding_service = EmbeddingService()

document_store = DocumentStore(
    embedding_service
)
```

Benefits:

- Loose coupling
- Easier testing
- Easier to replace implementations

---

# 8. FAISS

FAISS = **Facebook AI Similarity Search**

It is **not a database**.

It is a **vector index**.

---

## Before FAISS

```text
Query

↓

Loop through every embedding

↓

Cosine Similarity

↓

Sort
```

Complexity:

```
O(N)
```

---

## After FAISS

```text
Query

↓

FAISS Index

↓

Nearest Vectors

↓

Vector IDs

↓

Documents
```

The application does **not** know FAISS exists.

---

# 9. Why Normalize Embeddings?

Cosine Similarity:

```
A · B
-----------
||A|| ||B||
```

If every vector is normalized:

```
||A|| = ||B|| = 1
```

Then:

```
Cosine Similarity

=

Inner Product
```

Therefore:

- Normalize document embeddings
- Normalize query embeddings

Then FAISS `IndexFlatIP` performs cosine similarity search.

---

# 10. DocumentStore

Responsibilities:

- Store documents
- Store vectors
- Search vectors
- Count documents
- Clear storage

Public API:

```python
store.add_documents(documents, embeddings)

results = store.search(query_embedding)

count = store.count()

store.clear()
```

Internally it uses FAISS.

The application never knows.

---

# 11. SearchResult Data Class

Instead of:

```python
{
    "text": "...",
    "score": 0.91
}
```

We created:

```python
from dataclasses import dataclass

@dataclass
class SearchResult:
    text: str
    score: float
```

Access values like:

```python
result.text

result.score
```

instead of:

```python
result["text"]

result["score"]
```

Benefits:

- Autocomplete
- Type hints
- Cleaner code
- Easier to extend

---

# 12. Current Project Structure

```text
backend/

├── app.py
├── config.py
│
├── data/
│
├── embeddings/
│   ├── model.py
│   ├── service.py
│   └── vector_math.py
│
├── retrieval/
│   └── document_store.py
│
├── prompts/
│   ├── builder.py
│   └── templates.py
│
├── llm/
│   ├── client.py
│   └── generator.py
│
└── models/
    └── search_result.py
```

---

# 13. Why Good Architecture Matters

Changing the embedding model:

```
SentenceTransformer

↓

OpenAI Embeddings
```

Only `EmbeddingService` changes.

---

Changing the vector database:

```
FAISS

↓

Pinecone
```

Only `DocumentStore` changes.

---

Changing the LLM:

```
Qwen

↓

Llama
```

Only the LLM client changes.

Everything else remains untouched.

---

# 14. Software Engineering Principles Learned

- Single Responsibility Principle (SRP)
- Encapsulation
- Dependency Injection
- Separation of Concerns
- Abstraction
- Interface-first Design
- Clean Architecture

---

# Key Takeaways

- Retrieval and generation are different problems.
- Embedding models and LLMs have different responsibilities.
- FAISS is a vector index, not a database.
- Normalize embeddings before similarity search.
- Design APIs before implementations.
- Keep every module focused on one responsibility.
- Good architecture allows implementations to change without affecting the rest of the system.

---

# Current Project Status

- ✅ PDF Processing
- ✅ OCR Support
- ✅ Sentence Chunking
- ✅ Embedding Generation
- ✅ Semantic Search
- ✅ Prompt Builder
- ✅ Ollama Integration
- ✅ Local LLM
- ✅ FAISS Vector Index
- ✅ Dependency Injection
- ✅ SearchResult Data Class

---

# Upcoming Topics

- Document metadata
- PDF page tracking
- Source citations
- Better chunking strategies
- Hybrid Search (BM25 + FAISS)
- Query Expansion
- Cross-Encoder Reranking
- Persistent FAISS Index
- FastAPI Backend
- React Frontend
- Multi-document Collections