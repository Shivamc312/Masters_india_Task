from pdf2image import convert_from_path
from PIL import Image
import pytesseract


def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path, dpi=300)

def image_to_text(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)
