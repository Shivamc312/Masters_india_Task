import os
from utils import pdf_to_images, image_to_text
from extractors import GenericFieldExtractor
from pdf2image import convert_from_path

def pdf_to_images(pdf_path):
    poppler_path = r"C:\Users\ADMIN\Documents\poppler-24.08.0\Library\bin"
    return convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

CONFIG_PATH = r"C:\Users\ADMIN\Documents\invoice_extractor_2\fields_config.json"

def process_file(filepath, extractor):
    print(f"\n Processing: {filepath}")
    text = ""

    if filepath.lower().endswith(".pdf"):
        images = pdf_to_images(filepath)
        for img in images:
            text += image_to_text(img) + "\n"
    elif filepath.lower().endswith((".png", ".jpg", ".jpeg")):
        from PIL import Image
        img = Image.open(filepath)
        text = image_to_text(img)
    else:
        print(" Unsupported file type:", filepath)
        return

    invoice_data = extractor.extract_all_fields(text)
    invoice_data["raw_text"] = text[:500] + "..."

    print(" Extracted Fields:")
    for k, v in invoice_data.items():
        print(f"{k}: {v}\n")

def main():
    folder = r"C:\Users\ADMIN\Documents\invoice_extractor_2\invoices"
    extractor = GenericFieldExtractor(CONFIG_PATH)

    for file in os.listdir(folder):
        fullpath = os.path.join(folder, file)
        if os.path.isfile(fullpath):
            process_file(fullpath, extractor)

if __name__ == "__main__":
    main()
