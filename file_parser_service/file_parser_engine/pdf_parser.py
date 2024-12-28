from PIL import Image
import io
import fitz  # PyMuPDF
import hashlib
from collections import Counter

def remove_common_images(parsed_pdf, threshold=0.9):
    """
    Identifies and removes duplicate images based on their hash values.
    If over the threshold percentage of slides contain the same image,
    it is considered a duplicate and removed from the final list.
    
    Args:
        parsed_pdf (list): The parsed PDF data (slides with text and images).
        threshold (float): The percentage threshold to identify a trademark/placeholder image.
        
    Returns:
        list: Updated parsed PDF with unique images.
    """
    image_hashes = {}  # To store hashes and their frequencies
    image_contents = []  # To store image binary data
    unique_images = []  # To store unique images
    
    # Calculate the hashes for each image and track its frequency
    for slide in parsed_pdf:
        for img_bytes in slide["images"]:
            # Calculate image hash using MD5 (or any hashing algorithm)
            img_hash = hashlib.md5(img_bytes).hexdigest()
            
            if img_hash not in image_hashes:
                image_hashes[img_hash] = 0
                image_contents.append(img_bytes)
            
            # Increase frequency of the image hash
            image_hashes[img_hash] += 1
    
    # Determine if an image is too frequent (greater than threshold)
    total_slides = len(parsed_pdf)
    threshold_count = total_slides * threshold
    
    # Create a list of images to keep (those that don't exceed the threshold)
    for i, img_bytes in enumerate(image_contents):
        img_hash = hashlib.md5(img_bytes).hexdigest()
        if image_hashes[img_hash] < threshold_count:
            unique_images.append(img_bytes)

    # Now remove duplicate images from the parsed PDF slides
    for slide in parsed_pdf:
        slide["images"] = [img for img in slide["images"] if hashlib.md5(img).hexdigest() in [hashlib.md5(img_bytes).hexdigest() for img_bytes in unique_images]]
    
    return parsed_pdf

def remove_common_phrases(parsed_pdf, threshold=0.8):
    """
    Removes phrases that appear in more than the given percentage (threshold) of slides.
    
    :param parsed_pdf: List of slides, each with 'text' and 'images'
    :param threshold: Percentage of slides (e.g., 0.8 for 80%)
    :return: The updated parsed_pdf with common phrases removed
    """
    slide_texts = [slide["text"] for slide in parsed_pdf]
    total_slides = len(slide_texts)

    # Count occurrences of each phrase in the slides
    phrase_counts = {}
    for text in slide_texts:
        for phrase in text.splitlines():  # Split into lines to identify headers/footers
            phrase = phrase.strip()
            if phrase:
                phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

    # Identify phrases that exceed the threshold
    phrases_to_remove = {
        phrase for phrase, count in phrase_counts.items()
        if count / total_slides > threshold
    }

    # Remove identified phrases from all slides
    for slide in parsed_pdf:
        updated_text = "\n".join(
            line for line in slide["text"].splitlines()
            if line.strip() not in phrases_to_remove
        )
        slide["text"] = updated_text

    return parsed_pdf

def remove_uniform_images(parsed_pdf, threshold=0.95):
    """
    Removes images that are too uniform, e.g., contain 95% of the same pixel color.

    Args:
        parsed_pdf (list): The parsed PDF data (slides with text and images).
        threshold (float): Percentage threshold for pixel uniformity.

    Returns:
        list: Updated parsed PDF with uniform images removed.
    """
    def is_uniform_image(img_bytes, threshold):
        """Check if an image is uniform based on pixel data."""
        try:
            image = Image.open(io.BytesIO(img_bytes))
            image = image.convert("RGB")  # Ensure the image is in RGB format
            pixels = list(image.getdata())
            total_pixels = len(pixels)

            # Check if the image has valid pixel data
            if total_pixels == 0:
                return True  # Consider an empty image as uniform
            
            # Use Counter to efficiently count pixel occurrences
            pixel_counts = Counter(pixels)
            most_common_color, most_common_count = pixel_counts.most_common(1)[0]

            # Calculate uniformity percentage
            uniformity_percentage = most_common_count / total_pixels
            return uniformity_percentage >= threshold

        except Exception as e:
            print(f"Error processing image: {e}")
            return True  # Consider problematic images as uniform for safety


    # Remove uniform images from each slide
    for slide in parsed_pdf:
        slide["images"] = [img for img in slide["images"] if not is_uniform_image(img, threshold)]

    return parsed_pdf

def extract_text(page):
    """Extract text from a page."""
    return page.get_text("text")

def extract_images(page, pdf_document):
    """Extract images from a page and return them as a list of binary image data."""
    images = []
    image_list = page.get_images(full=True)
    
    for img_index, img in enumerate(image_list):
        xref = img[0]  # Image reference
        base_image = pdf_document.extract_image(xref)
        img_bytes = base_image["image"]  # Raw image bytes
        images.append(img_bytes)
    
    return images

def parse_pdf(pdf_path):
    """Parse a PDF, extracting text and images from each page and return an array of objects."""
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    slides = []

    # Loop through each page of the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Extract text and images for the page
        text = extract_text(page)
        images = extract_images(page, pdf_document)
        
        # Create a slide object with text and images
        slide = {
            "text": text,
            "images": images
        }

        # Append the slide to the slides array
        slides.append(slide)

    # Preprocessing pipeline
    parsed_pdf = remove_common_images(slides)
    parsed_pdf = remove_common_phrases(parsed_pdf)
    parsed_pdf = remove_uniform_images(parsed_pdf)  # Add uniform image removal here
    
    return parsed_pdf
