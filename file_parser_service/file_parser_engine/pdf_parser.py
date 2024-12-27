from PyPDF2 import PdfReader

def parse_pdf(file_path):
    """
    Parses a PDF to extract raw text and metadata.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        dict: Extracted slides and metadata.
    """
    reader = PdfReader(file_path)
    slides = []

    for page in reader.pages:
        text = page.extract_text() or ""
        slides.append({"text": text, "images": None})  # Placeholder for images

    return {"slides": slides, "metadata": reader.metadata}