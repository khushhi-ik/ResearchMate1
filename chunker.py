def chunk_pages(pages, chunk_size=1200, overlap=180):
    """Split each page into overlapping character chunks, retaining page metadata."""
    chunks = []
    for page in pages:
        text = page["text"]
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            piece = text[start:end].strip()
            if piece:
                chunks.append({"text": piece, "page": page["page"]})
            if end >= len(text):
                break
            start = end - overlap
    return chunks
