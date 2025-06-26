import cv2
import pytesseract
from PIL import Image
import numpy as np
import glob
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\zabit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def process_scoreboard_image(image_path, scoreboard_name):
    """Apply OCR to a scoreboard image and return the extracted text."""
    print(f"\nProcessing {scoreboard_name}: {image_path}")
    
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not load image {image_path}")
            return None
        
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
        
        print(f"{scoreboard_name} OCR Result:")
        print(f"Extracted Text: {repr(text)}")
        print(f"Clean Text: {text.strip()}")
        
        return text.strip()
        
    except Exception as e:
        print(f"Error processing {scoreboard_name}: {e}")
        return None

# Find the newest red_scoreboard.png and blue_scoreboard.png files
red_files = glob.glob('red_scoreboard.png')
blue_files = glob.glob('blue_scoreboard.png')

results = {}

# Process red scoreboard
if red_files:
    red_image_path = max(red_files, key=os.path.getmtime)
    red_text = process_scoreboard_image(red_image_path, "Red Scoreboard")
    results['red'] = red_text
else:
    print("No red_scoreboard.png file found in the current directory")
    results['red'] = None

# Process blue scoreboard  
if blue_files:
    blue_image_path = max(blue_files, key=os.path.getmtime)
    blue_text = process_scoreboard_image(blue_image_path, "Blue Scoreboard")
    results['blue'] = blue_text
else:
    print("No blue_scoreboard.png file found in the current directory")
    results['blue'] = None

# Save results to text files
if results['red'] is not None:
    with open('red_scoreboard.txt', 'w') as f:
        f.write(results['red'])
    print(f"Saved red scoreboard text to red_scoreboard.txt")
else:
    print("No red scoreboard text to save")

if results['blue'] is not None:
    with open('blue_scoreboard.txt', 'w') as f:
        f.write(results['blue'])
    print(f"Saved blue scoreboard text to blue_scoreboard.txt")
else:
    print("No blue scoreboard text to save")