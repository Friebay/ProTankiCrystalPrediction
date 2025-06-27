import cv2
import pytesseract
from PIL import Image
import numpy as np
import glob
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\zabit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Debug toggle - Set to True to save processing step images, False to skip
DEBUG = True

def clean_extracted_text(text):
    """Remove all text after the first line that contains only '0' and remove multiple consecutive newlines."""
    if not text:
        return text
    
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Check if the line contains only '0' (ignoring whitespace)
        if line.strip() == '0':
            # Found the first line with only '0', stop here
            break
        cleaned_lines.append(line)
    
    # Join lines and remove multiple consecutive newlines
    result = '\n'.join(cleaned_lines)
    
    # Replace multiple consecutive newlines with single newlines
    import re
    result = re.sub(r'\n\s*\n+', '\n', result)
    
    return result

def process_scoreboard_image(image_path, scoreboard_name):
    """Apply OCR to a scoreboard image and return the extracted text."""
    print(f"\nProcessing {scoreboard_name}: {image_path}")
    
    try:
        # Create debug directory if DEBUG is enabled
        if DEBUG:
            debug_dir = r"C:\Users\zabit\Documents\GitHub\ProTankiCrystalPrediction\processing_steps"
            os.makedirs(debug_dir, exist_ok=True)
            
            # Create a clean name for debug files
            clean_name = scoreboard_name.lower().replace(" ", "_")
        
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not load image {image_path}")
            return None
        
        if DEBUG:
            debug_original = os.path.join(debug_dir, f"images\\{clean_name}_01_original.png")
            cv2.imwrite(debug_original, img)
            print(f"Debug: Saved original image to {debug_original}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        if DEBUG:
            debug_gray = os.path.join(debug_dir, f"images\\{clean_name}_02_grayscale.png")
            cv2.imwrite(debug_gray, gray)
            print(f"Debug: Saved grayscale image to {debug_gray}")
        
        # Resize image for better OCR accuracy
        scale_factor = 3  # Increase resolution
        resized = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        if DEBUG:
            debug_resized = os.path.join(debug_dir, f"images\\{clean_name}_03_resized.png")
            cv2.imwrite(debug_resized, resized)
            print(f"Debug: Saved resized image to {debug_resized}")
        
        # Apply thresholding for better contrast
        _, thresh = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY_INV)
        
        if DEBUG:
            debug_thresh = os.path.join(debug_dir, f"images\\{clean_name}_04_threshold.png")
            cv2.imwrite(debug_thresh, thresh)
            print(f"Debug: Saved threshold image to {debug_thresh}")
        
        # Invert image if necessary (dark text on light bg)
        thresh = cv2.bitwise_not(thresh)
        
        if DEBUG:
            debug_final = os.path.join(debug_dir, f"images\\{clean_name}_05_final_processed.png")
            cv2.imwrite(debug_final, thresh)
            print(f"Debug: Saved final processed image to {debug_final}")
        
        # Run Tesseract OCR
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(thresh, config=custom_config)
        
        # Clean the extracted text by removing everything after the first line with only '0'
        cleaned_text = clean_extracted_text(text.strip())
        
        print(f"{scoreboard_name} OCR Result:")
        print(f"Extracted Text: {repr(text)}")
        print(f"Cleaned Text: {repr(cleaned_text)}")
        
        return cleaned_text
        
    except Exception as e:
        print(f"Error processing {scoreboard_name}: {e}")
        return None

# Find the newest red_scoreboard.png and blue_scoreboard.png files
red_files = glob.glob('images\\red_scoreboard.png')
blue_files = glob.glob('images\\blue_scoreboard.png')

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