import os
import pytesseract
from PIL import Image

def ocr_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

def perform_ocr(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return ""

    if not file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        print(f"File {file_path} is not a supported image format.")
        return ""

    return ocr_image(file_path)

if __name__ == "__main__":
    input_directory = os.path.join(os.path.expanduser("~/Desktop"), "SiloV2/SH")
    main(input_directory)
