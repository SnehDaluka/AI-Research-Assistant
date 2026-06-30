# RAG (Retrieval-Augmented Generation)

## What is RAG?

RAG is a technique where we retrieve relevant information from external documents before asking an LLM to generate an answer.

Instead of relying only on the model's training data, we provide additional context.

---

## Workflow

```text
Upload PDF
      ↓
Extract Text
      ↓
Chunk Text
      ↓
Generate Embeddings
      ↓
Store Embeddings
--------------------------
User Question
      ↓
Question Embedding
      ↓
Similarity Search
      ↓
Retrieve Relevant Chunks
      ↓
LLM
      ↓
Answer
```

---

## Why use RAG?

Without RAG:

- LLM may hallucinate
- Cannot answer questions about private documents
- Limited to training knowledge

With RAG:

- Uses company documents
- More accurate
- Can cite sources

---

## Key Takeaways

- RAG combines retrieval and generation.
- The LLM answers using retrieved context.
- Retrieval quality directly affects answer quality.