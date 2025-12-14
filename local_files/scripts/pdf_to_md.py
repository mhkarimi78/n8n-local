# scripts/pdf_to_md.py
from docling.document_converter import DocumentConverter
import sys, os

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    md_path = pdf_path.replace(".pdf", ".md")
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(result.document.export_to_markdown())
    print(md_path)