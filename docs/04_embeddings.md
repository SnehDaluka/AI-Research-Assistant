# Embeddings

## Problem

Computers do not understand meaning.

```
Dog

≠

Puppy
```

They are different strings.

---

## Solution

Convert text into vectors.

```
"I love dogs"

↓

[0.24, -0.61, ...]
```

---

## Definition

An embedding is a numerical representation of meaning.

Semantically similar sentences have vectors that are close together.

---

## Generate Embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

embeddings = model.encode(sentences)
```

---

## Why Embeddings?

Keyword Search:

```
Search:

puppy
```

Document:

```
dog
```

No match.

Embedding Search:

```
dog ≈ puppy
```

Match found.

---

## Important Notes

Embeddings are coordinates in semantic space.

They do not directly describe the sentence.

They indicate where the sentence lies relative to others.