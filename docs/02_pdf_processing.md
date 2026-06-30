# PDF Processing

## Problem

A PDF is not stored as plain text.

It contains:

- Text
- Fonts
- Images
- Coordinates
- Layout

---

## Reading PDFs

```python
from pypdf import PdfReader

reader = PdfReader("sample.pdf")
```

---

## Extract Text

```python
for page in reader.pages:
    text = page.extract_text()
```

---

## Store Metadata

```python
{
    "page": 1,
    "text": "...",
    "characters": 1200,
    "words": 215
}
```

---

## Image PDFs

Scanned PDFs contain only images.

```
PDF

↓

Image
```

Result:

```python
extract_text()

↓

None
```

OCR is required.