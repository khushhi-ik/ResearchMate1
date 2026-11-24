import fitz

def extract_pdf(uploaded_file):
    """Extract selectable text from each PDF page while preserving page numbers."""
    data = uploaded_file.getvalue()
    document = fitz.open(stream=data, filetype="pdf")
    pages = []
    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()
        if text:
            pages.append({"page": page_number, "text": text})
    document.close()
    return pages
