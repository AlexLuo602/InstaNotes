# parse_image.py

from pdf2image import convert_from_path

def parse_image(file_path):
    """
    Extracts images from the PDF for each slide.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        list: A list of images (as PIL Image objects) for each slide.
    """
    # Convert the PDF to a list of images, one for each page
    images = convert_from_path(file_path)

    # Here, you can return the images as is or do any processing you need
    # For example, you could save them as files or just keep them in memory
    return images
