import cv2
import pytesseract
from PIL import Image
import numpy as np
import glob
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\zabit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Find the newest diamond_crop_ PNG file
diamond_files = glob.glob('diamond_crop_*.png')
if not diamond_files:
    raise FileNotFoundError("No diamond_crop_ PNG files found in the current directory")

# Get the newest file based on modification time
image_path = max(diamond_files, key=os.path.getmtime)
print(f"Using image: {image_path}")

# Load image
img = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Resize image for better OCR accuracy
scale_factor = 3  # Increase resolution
resized = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

# Apply thresholding for better contrast
_, thresh = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY_INV)

# Invert image if necessary (dark text on light bg)
thresh = cv2.bitwise_not(thresh)

# Run Tesseract OCR
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
text = pytesseract.image_to_string(thresh, config=custom_config)

print("Extracted Text:", text)

# Save the extracted text to battle_fund.txt
with open('battle_fund.txt', 'w') as f:
    f.write(text.strip())
print("Saved extracted text to battle_fund.txt")
