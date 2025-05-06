import pytesseract
from PIL import Image
import PyPDF2

def process_image(image_file):
    """Extracts text from an uploaded image using OCR."""
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text if text.strip() else "No readable text found in the image."

def process_pdf(pdf_file):
    """Extracts text from a PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text if text.strip() else "No readable text found in the PDF."

def process_input(input_type, file):
    """Processes input based on type."""
    if input_type == "Image":
        return process_image(file)
    elif input_type == "PDF":
        return process_pdf(file)
    return None
