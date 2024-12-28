# parse_text.py

from PyPDF2 import PdfReader

def parse_text(file_path):
    """
    Extracts raw text from the PDF for each slide.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        list: A list of strings, where each string is the text from one slide.
    """
    reader = PdfReader(file_path)
    text_data = []

    for page in reader.pages:
        text = page.extract_text() or ""
        text_data.append(text)

    return text_data
