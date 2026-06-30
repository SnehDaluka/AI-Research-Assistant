from pathlib import Path
from pypdf import PdfReader


def extract_text(pdf_path: str):
    print("Current Working Directory:", Path.cwd())
    print("Looking for:", pdf_file.resolve())
    print("Exists:", pdf_file.exists())
    
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        
        print(f"Page {page_number}")
        print(f"Characters: {len(text)}")
        print(f"Words: {len(text.split())}")
        print("-" * 40)
        
        if text is None:
            text = ""

        pages.append({
            "page": page_number,
            "text": text,
            "characters": len(text),
            "words": len(text.split())
        })

    return pages


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    pdf_file = BASE_DIR / "data" / "sample.pdf"

    pages = extract_text(pdf_file)

    for page in pages:
        print("=" * 50)
        print(f"Page {page['page']}")
        print(page["text"])