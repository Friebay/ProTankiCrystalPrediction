import cv2
import numpy as np
import pytesseract
import glob
import os
from datetime import datetime

# --- Configuration ---

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\zabit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Tesseract configuration for reading only digits from a single line of text
TESSERACT_CONFIG = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'

def get_team_scores(image_path, debug=False):
    """
    Analyzes an image to find and OCR team scores based on color.

    Args:
        image_path (str): The path to the input image file.
        debug (bool): If True, saves intermediate processing images. Default is False.

    Returns:
        dict: A dictionary containing the 'red_score' and 'blue_score'.
              Returns None for a score if it cannot be read.
    """
    # Create output directory for step images only if debug is enabled
    if debug:
        output_dir = "processing_steps"
        os.makedirs(output_dir, exist_ok=True)
        # Extract base filename for naming output images
        base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # 1. Load the image
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image from path: {image_path}")
            return None
    except Exception as e:
        print(f"An error occurred while loading the image: {e}")
        return None

    # Save step 1: Original image
    if debug:
        step1_path = os.path.join(output_dir, f"images\\{base_name}_step1_original.png")
        cv2.imwrite(step1_path, img)
        print(f"Step 1 - Original image saved: {step1_path}")

    # 2. Convert the image from BGR to HSV color space
    # HSV is better for color segmentation than RGB/BGR.
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Save step 2: HSV image
    if debug:
        step2_path = os.path.join(output_dir, f"images\\{base_name}_step2_hsv.png")
        cv2.imwrite(step2_path, hsv_img)
        print(f"Step 2 - HSV image saved: {step2_path}")

    # 3. Define color ranges in HSV
    # The user-provided HEX codes are a great start. We convert them to HSV
    # and define a range around them.
    # Note: In OpenCV, Hue is 0-179, Saturation is 0-255, Value is 0-255.

    # --- RED TEAM SCORE ---
    # Red wraps around the 0/180 degree mark in the HSV color space, so we need two ranges.
    lower_red1 = np.array([5, 153, 200])
    upper_red1 = np.array([8, 207, 255])
    lower_red2 = np.array([170, 100, 150])
    upper_red2 = np.array([179, 255, 255])

    # --- BLUE TEAM SCORE ---
    lower_blue = np.array([103, 173, 150])
    upper_blue = np.array([108, 204, 255])

    # 4. Create masks to isolate colors
    red_mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2) # Combine the two red ranges

    blue_mask = cv2.inRange(hsv_img, lower_blue, upper_blue)
    
    # Save step 3: Color masks
    if debug:
        step3a_path = os.path.join(output_dir, f"images\\{base_name}_step3a_red_mask1.png")
        cv2.imwrite(step3a_path, red_mask1)
        print(f"Step 3a - Red mask 1 saved: {step3a_path}")
        
        step3b_path = os.path.join(output_dir, f"images\\{base_name}_step3b_red_mask2.png")
        cv2.imwrite(step3b_path, red_mask2)
        print(f"Step 3b - Red mask 2 saved: {step3b_path}")
        
        step3c_path = os.path.join(output_dir, f"images\\{base_name}_step3c_red_mask_combined.png")
        cv2.imwrite(step3c_path, red_mask)
        print(f"Step 3c - Combined red mask saved: {step3c_path}")
        
        step3d_path = os.path.join(output_dir, f"images\\{base_name}_step3d_blue_mask.png")
        cv2.imwrite(step3d_path, blue_mask)
        print(f"Step 3d - Blue mask saved: {step3d_path}")

    # 5. OCR the numbers from each mask
    red_score_str = ocr_from_mask(red_mask, output_dir if debug else None, base_name if debug else None, "red", debug)
    blue_score_str = ocr_from_mask(blue_mask, output_dir if debug else None, base_name if debug else None, "blue", debug)
    
    # 6. Convert string results to integers, handling potential errors
    try:
        red_score = int(red_score_str) if red_score_str else None
    except (ValueError, TypeError):
        red_score = None # Or 0, or some other default

    try:
        blue_score = int(blue_score_str) if blue_score_str else None
    except (ValueError, TypeError):
        blue_score = None

    return {
        "red_score": red_score,
        "blue_score": blue_score
    }

def ocr_from_mask(mask, output_dir, base_name, color_name, debug=False):
    """
    Helper function to perform OCR on a binary mask image.
    """
    # The mask is already a single-channel image perfect for Tesseract.
    # We can optionally add some processing like dilation to make characters thicker.
    kernel = np.ones((2, 2), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=1)
    
    # Save step 4: Dilated mask
    if debug and output_dir and base_name:
        step4_path = os.path.join(output_dir, f"images\\{base_name}_step4_{color_name}_dilated.png")
        cv2.imwrite(step4_path, dilated_mask)
        print(f"Step 4 - {color_name.capitalize()} dilated mask saved: {step4_path}")
    
    # Invert the mask because Tesseract prefers black text on a white background.
    # Our mask has white text on a black background.
    inverted_mask = cv2.bitwise_not(dilated_mask)
    
    # Save step 5: Inverted mask ready for OCR
    if debug and output_dir and base_name:
        step5_path = os.path.join(output_dir, f"images\\{base_name}_step5_{color_name}_inverted_for_ocr.png")
        cv2.imwrite(step5_path, inverted_mask)
        print(f"Step 5 - {color_name.capitalize()} inverted mask for OCR saved: {step5_path}")
    
    # Resize the image to be 2x bigger for better OCR accuracy
    height, width = inverted_mask.shape
    resized_mask = cv2.resize(inverted_mask, (width * 3, height * 3), interpolation=cv2.INTER_NEAREST)
    
    # Save step 6: Resized mask for OCR
    if debug and output_dir and base_name:
        step6_path = os.path.join(output_dir, f"images\\{base_name}_step6_{color_name}_resized_2x_for_ocr.png")
        cv2.imwrite(step6_path, resized_mask)
        print(f"Step 6 - {color_name.capitalize()} resized 2x mask for OCR saved: {step6_path}")

    try:
        # Perform OCR using the specific configuration on the resized image
        text = pytesseract.image_to_string(resized_mask, config=TESSERACT_CONFIG)
        # Clean up any whitespace or non-digit characters that might slip through
        cleaned_text = "".join(filter(str.isdigit, text))
        if debug:
            print(f"OCR result for {color_name}: '{text}' -> cleaned: '{cleaned_text}'")
        return cleaned_text
    except pytesseract.TesseractNotFoundError:
        print("Tesseract Error: The Tesseract executable was not found.")
        print("Please make sure Tesseract is installed and configured in your system's PATH.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during OCR: {e}")
        return None

def save_scores_to_files(scores):
    """
    Save the red and blue scores to separate text files with timestamp logging.
    
    Args:
        scores (dict): Dictionary containing 'red_score' and 'blue_score' keys
    """
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save red score to file
        red_score_file = os.path.join(script_dir, "red_score.txt")
        red_score_value = str(scores['red_score']) if scores['red_score'] is not None else "N/A"
        with open(red_score_file, 'w') as f:
            f.write(red_score_value)
        print(f"Red score saved to: {red_score_file}")
        
        # Save blue score to file
        blue_score_file = os.path.join(script_dir, "blue_score.txt")
        blue_score_value = str(scores['blue_score']) if scores['blue_score'] is not None else "N/A"
        with open(blue_score_file, 'w') as f:
            f.write(blue_score_value)
        print(f"Blue score saved to: {blue_score_file}")
        
        # Save combined scores with timestamp to a log file
        scores_log_file = os.path.join(script_dir, "scores_log.txt")
        with open(scores_log_file, 'a') as f:
            f.write(f"{timestamp} - Red: {red_score_value}, Blue: {blue_score_value}\n")
        print(f"Scores logged to: {scores_log_file}")
        
    except Exception as e:
        print(f"Error saving scores to files: {e}")

# --- Main execution ---
if __name__ == "__main__":
    # Set debug mode - change to True if you want to save processing step images
    debug = True

    # Find the newest flag_crop PNG file
    flag_files = glob.glob('images\\flag_crop.png')
    if not flag_files:
        raise FileNotFoundError("No flag_crop PNG files found in the current directory")

    # Get the newest file based on modification time
    image_path = max(flag_files, key=os.path.getmtime)
    print(f"Using image: {image_path}")

    scores = get_team_scores(image_path, debug=debug)

    if scores:
        # print("\n--- OCR Results ---")
        # print(f"Red Team Score: {scores['red_score']}")
        # print(f"Blue Team Score: {scores['blue_score']}")
        
        # Save scores to text files
        save_scores_to_files(scores)
        
        if debug:
            print(f"\nAll processing step images have been saved to the 'processing_steps' directory.")
    else:
        print("Failed to process the image.")