from PIL import Image
import pytesseract
import os
from pathlib import Path

# Open an image using PIL (Pillow)
image = Image.open(Path(__file__).resolve().parent / "1-8.jpg")

# Perform OCR on the image
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
