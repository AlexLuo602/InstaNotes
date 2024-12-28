import os
import unittest
from file_parser_engine.pdf_parser import parse_pdf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import io

class TestFileParserEngine(unittest.TestCase):
    def setUp(self):
        # Set up the paths for resources and output directories
        self.resources_folder = os.path.join(os.path.dirname(__file__), "resources")
        self.output_folder = os.path.join(os.path.dirname(__file__), "output")
        
        # Ensure the output directory exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    
            
    def test_cpsc_344_design_concepts(self):
        # Parse the PDF
        pdf_path = os.path.join(self.resources_folder, "cpsc_344_design_concepts.pdf")
        parsed_pdf = parse_pdf(pdf_path)

        # Generate the new PDF file
        output_pdf_path = os.path.join(self.output_folder, "cpsc_344_design_concepts_output.pdf")
        c = canvas.Canvas(output_pdf_path, pagesize=letter)

        width, height = letter  # Default page size

        for slide_index, slide in enumerate(parsed_pdf, start=1):
            text = slide["text"]
            images = slide["images"]
            
            # Start by writing the text to the PDF
            c.setFont("Helvetica", 10)
            text_object = c.beginText(40, height - 40)  # Start from top left corner
            text_object.textLines(text)
            c.drawText(text_object)

            # Position the images beside the text
            x_offset_for_images = 300  # Start placing images to the right of the text area
            y_offset_for_images = height - 150  # Start placing images below the text
            for img_index, img_bytes in enumerate(images):
                # Convert binary data to PIL Image
                image = Image.open(io.BytesIO(img_bytes))
                image_path = os.path.join(self.output_folder, f"image_slide_{slide_index}_{img_index+1}.png")
                image.save(image_path, format="PNG")
                
                # Draw the image onto the PDF (side by side with the text)
                c.drawImage(image_path, x_offset_for_images, y_offset_for_images, width=200, height=150)
                y_offset_for_images -= 160  # Adjust y-position for the next image
                os.remove(image_path)

            # Add a new page after each slide if there are multiple slides
            c.showPage()

        # Save the generated PDF
        c.save()

        # Check that the output PDF file was created
        self.assertTrue(os.path.exists(output_pdf_path))

    def test_cpsc_310_process(self):
        # Parse the PDF
        pdf_path = os.path.join(self.resources_folder, "cpsc_310_process.pdf")
        parsed_pdf = parse_pdf(pdf_path)

        # Generate the new PDF file
        output_pdf_path = os.path.join(self.output_folder, "cpsc_310_process_output.pdf")
        c = canvas.Canvas(output_pdf_path, pagesize=letter)

        width, height = letter  # Default page size

        for slide_index, slide in enumerate(parsed_pdf, start=1):
            text = slide["text"]
            images = slide["images"]
            
            # Start by writing the text to the PDF
            c.setFont("Helvetica", 10)
            text_object = c.beginText(40, height - 40)  # Start from top left corner
            text_object.textLines(text)
            c.drawText(text_object)

            # Position the images beside the text
            x_offset_for_images = 300  # Start placing images to the right of the text area
            y_offset_for_images = height - 150  # Start placing images below the text
            for img_index, img_bytes in enumerate(images):
                # Convert binary data to PIL Image
                image = Image.open(io.BytesIO(img_bytes))
                image_path = os.path.join(self.output_folder, f"image_slide_{slide_index}_{img_index+1}.png")
                image.save(image_path, format="PNG")
                
                # Draw the image onto the PDF (side by side with the text)
                c.drawImage(image_path, x_offset_for_images, y_offset_for_images, width=200, height=150)
                y_offset_for_images -= 160  # Adjust y-position for the next image
                os.remove(image_path)

            # Add a new page after each slide if there are multiple slides
            c.showPage()

        # Save the generated PDF
        c.save()

        # Check that the output PDF file was created
        self.assertTrue(os.path.exists(output_pdf_path))

if __name__ == '__main__':
    unittest.main()
