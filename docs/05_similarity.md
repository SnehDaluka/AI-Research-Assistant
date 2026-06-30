# Similarity Search

## Goal

Compare two embeddings.

---

## Cosine Similarity

Measures the angle between vectors.

```
1

↓

Exactly similar
```

```
0

↓

Unrelated
```

```
-1

↓

Opposite
```

---

## Code

```python
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(embeddings)
```

---

## Example

```
"I love dogs"

"I like puppies"

↓

0.84
```

High similarity.

---

## Observations

Technology companies are close.

Fruits are close.

Synonyms are close.

Meaning matters more than exact words.