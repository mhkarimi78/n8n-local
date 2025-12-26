# فایل: pdf_converter.py
from docling.document_converter import DocumentConverter

def process_report_from_url(pdf_url: str):
    """
    لینک PDF را دریافت می‌کند و با استفاده از Docling متن آن را استخراج می‌کند.
    """
    try:
        converter = DocumentConverter()
        result = converter.convert(pdf_url)
        markdown_output = result.document.export_to_markdown()
        return markdown_output
        
    except Exception as e:
        return f"خطا در پردازش سند: {str(e)}"

if __name__ == "__main__":
    # برای تست
    url = "https://lines.coscoshipping.com/lines_resource/pdf/quality2023en.pdf"
    text_content = process_report_from_url(url)
    print(text_content[:2000])  # نمایش 2000 کاراکتر اول