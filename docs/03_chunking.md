# Chunking

## Why Chunk?

LLMs cannot efficiently process entire books or very large documents.

Instead:

```
Document

↓

Chunks
```

---

## Simple Chunking

```python
def chunk_text(text, chunk_size=100):
```

Split after a fixed number of words.

---

## Problem

Chunks may split sentences.

Example:

```
Artificial Intelligence is changing the

world by automating...
```

Meaning is lost.

---

## Overlap

```
Chunk 1

Artificial Intelligence is changing the

Chunk 2

is changing the world by automating
```

Overlap preserves context.

---

## Code

```python
def chunk_text(text, chunk_size=100, overlap=20):
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunks.append(" ".join(words[i:i+chunk_size]))

    return chunks
```

---

## Types of Chunking

- Word-based
- Sentence-based
- Paragraph-based
- Recursive
- Semantic

Each has trade-offs.