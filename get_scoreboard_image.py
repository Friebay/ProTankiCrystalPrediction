import pyautogui
import os
from datetime import datetime
import time
import keyboard  # Added for key press detection
import cv2
import numpy as np
import subprocess
import sys

# OCR Toggle - Set to True to run OCR processing, False to skip it
OCR = True

def find_score_images_in_screenshot(screenshot_path):
    """Find score_red.png and score_blue.png templates in the screenshot and return their coordinates."""
    results = {}
    
    # Score image files to search for
    score_images = ['images\\score_red.png', 'images\\score_blue.png']
    
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load the screenshot once
        screenshot = cv2.imread(screenshot_path)
        if screenshot is None:
            print(f"Could not load screenshot: {screenshot_path}")
            return None
        
        for score_image in score_images:
            template_path = os.path.join(script_dir, score_image)
            
            # Check if template exists
            if not os.path.exists(template_path):
                print(f"Template file not found: {template_path}")
                results[score_image] = None
                continue
            
            # Load the template
            template = cv2.imread(template_path)
            
            if template is None:
                print(f"Could not load template: {template_path}")
                results[score_image] = None
                continue
            
            # Get template dimensions
            template_height, template_width = template.shape[:2]
            
            # Perform template matching
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            
            # Find the best match
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # Set a threshold for matching (adjust as needed)
            threshold = 0.8
            
            if max_val >= threshold:
                # Calculate center coordinates of the found object
                top_left = max_loc
                center_x = top_left[0] + template_width // 2
                center_y = top_left[1] + template_height // 2
                
                # print(f"{score_image} found at coordinates: ({center_x}, {center_y})")
                # print(f"Match confidence: {max_val:.3f}")
                # print(f"Top-left corner: {top_left}")
                # print(f"Bottom-right corner: ({top_left[0] + template_width}, {top_left[1] + template_height})")
                
                results[score_image] = {
                    'center': (center_x, center_y),
                    'top_left': top_left,
                    'bottom_right': (top_left[0] + template_width, top_left[1] + template_height),
                    'confidence': max_val
                }
            else:
                print(f"{score_image} not found. Best match confidence: {max_val:.3f} (threshold: {threshold})")
                results[score_image] = None
        
        return results
            
    except Exception as e:
        print(f"Error finding score images in screenshot: {e}")
        return None

def find_exit_image_in_screenshot(screenshot_path):
    """Find exit.png template in the screenshot and return its coordinates."""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load the screenshot
        screenshot = cv2.imread(screenshot_path)
        if screenshot is None:
            print(f"Could not load screenshot: {screenshot_path}")
            return None
        
        template_path = os.path.join(script_dir, "images\\exit.png")
        
        # Check if template exists
        if not os.path.exists(template_path):
            print(f"Template file not found: {template_path}")
            return None
        
        # Load the template
        template = cv2.imread(template_path)
        
        if template is None:
            print(f"Could not load template: {template_path}")
            return None
        
        # Get template dimensions
        template_height, template_width = template.shape[:2]
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        
        # Find the best match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Set a threshold for matching (adjust as needed)
        threshold = 0.8
        
        if max_val >= threshold:
            # Calculate center coordinates of the found object
            top_left = max_loc
            center_x = top_left[0] + template_width // 2
            center_y = top_left[1] + template_height // 2
            
            print(f"exit.png found at coordinates: ({center_x}, {center_y})")
            print(f"Match confidence: {max_val:.3f}")
            print(f"Top-left corner: {top_left}")
            print(f"Bottom-right corner: ({top_left[0] + template_width}, {top_left[1] + template_height})")
            
            return {
                'center': (center_x, center_y),
                'top_left': top_left,
                'bottom_right': (top_left[0] + template_width, top_left[1] + template_height),
                'confidence': max_val
            }
        else:
            print(f"exit.png not found. Best match confidence: {max_val:.3f} (threshold: {threshold})")
            return None
            
    except Exception as e:
        print(f"Error finding exit image in screenshot: {e}")
        return None

def take_screenshot():
    """Take a screenshot of a specific region and save it in the script directory."""
    try:
        # Take a screenshot of the entire screen
        screenshot = pyautogui.screenshot()
        
        # Get screen width and height
        screen_width, screen_height = screenshot.size
        
        # First, take a temporary full screenshot to find the exit image
        temp_filename = f"images\\temp_screenshot.png"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_filepath = os.path.join(script_dir, temp_filename)
        screenshot.save(temp_filepath, format='PNG', optimize=False, compress_level=0, quality=100)
        
        # Find exit image in the full screenshot
        print("Searching for exit image to determine crop boundaries...")
        exit_result = find_exit_image_in_screenshot(temp_filepath)
        
        # Delete temporary file
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        
        # Determine crop boundaries
        if exit_result:
            # Use exit image's top-left corner as the bottom boundary
            crop_bottom = exit_result['top_left'][1]
            print(f"Exit image found! Cropping bottom boundary set to y={crop_bottom}")
        else:
            # Fallback to original bottom boundary if exit image not found
            crop_bottom = 1080
            print("Exit image not found. Using default bottom boundary.")
        
        # Crop the image to the specified region (from x=0 to right edge, y=0 to exit image top)
        cropped_screenshot = screenshot.crop((872, 38, 1269, crop_bottom))
        
        filename = f"images\\scoreboard_image.png"
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
        
        # Save the cropped screenshot in highest quality (raw/uncompressed)
        cropped_screenshot.save(filepath, format='PNG', optimize=False, compress_level=0, quality=100)
        
        print("Playing sound notification...")
        # Play MP3 file
        try:
            import pygame
            pygame.mixer.init()
            # Assuming screenshot.mp3 is in the same directory as the script
            sound_path = os.path.join(script_dir, "sounds\\screenshot.mp3")
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            # Wait for the sound to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
        except Exception as sound_error:
            print(f"Could not play sound: {sound_error}")
        
        print(f"Cropped screenshot saved as: {filepath}")
        
        # Find exit image in the cropped screenshot (for verification)
        print("Verifying exit image location in cropped screenshot...")
        exit_result_cropped = find_exit_image_in_screenshot(filepath)
        
        # Find score images in the screenshot
        print("Searching for score images in the screenshot...")
        score_results = find_score_images_in_screenshot(filepath)
        
        if score_results:
            print("Score image detection completed!")
            
            # Print locations of found score images
            '''
            for score_image, result in score_results.items():
                if result:
                    print(f"\n{score_image} location details:")
                    print(f"  Center coordinates: {result['center']}")
                    print(f"  Top-left corner: {result['top_left']}")
                    print(f"  Bottom-right corner: {result['bottom_right']}")
                    print(f"  Match confidence: {result['confidence']:.3f}")
                else:
                    print(f"\n{score_image}: Not found in screenshot")
            '''
            # Create additional crops if both score images are found
            red_result = score_results.get('images\\score_red.png')
            blue_result = score_results.get('images\\score_blue.png')

            if red_result and blue_result:
                print("\nCreating scoreboard crops...")
                
                # Take a fresh screenshot for cropping (using the original cropped area coordinates)
                full_screenshot = pyautogui.screenshot()
                
                # Adjust coordinates to account for the original crop offset (872, 38)
                crop_offset_x = 872
                crop_offset_y = 38
                
                # Calculate absolute coordinates on the full screen
                red_bottom_left_x = crop_offset_x + red_result['bottom_right'][0] - (red_result['bottom_right'][0] - red_result['top_left'][0])  # left edge
                red_bottom_left_y = crop_offset_y + red_result['bottom_right'][1] + 4  # bottom edge

                blue_top_right_x = crop_offset_x + blue_result['bottom_right'][0] + 4  # right edge
                blue_top_right_y = crop_offset_y + blue_result['top_left'][1]  # top edge
                
                blue_bottom_right_x = 974
                blue_bottom_right_y = 1080
                
                # Create red_scoreboard.png (from red bottom-left to blue top-right)
                red_crop = full_screenshot.crop((red_bottom_left_x, red_bottom_left_y, blue_top_right_x, blue_top_right_y))
                red_scoreboard_path = os.path.join(script_dir, "images\\red_scoreboard.png")
                red_crop.save(red_scoreboard_path, format='PNG', optimize=False, compress_level=0, quality=100)
                # print(f"Red scoreboard saved as: {red_scoreboard_path}")
                # print(f"Red crop coordinates: ({red_bottom_left_x}, {red_bottom_left_y}) to ({blue_top_right_x}, {blue_top_right_y})")
                
                # Create blue_scoreboard.png (from blue location to 974, 1080)
                blue_top_left_x = crop_offset_x + blue_result['top_left'][0]
                blue_top_left_y = crop_offset_y + blue_result['top_left'][1] + 19

                blue_crop = full_screenshot.crop((blue_top_left_x, blue_top_left_y, blue_bottom_right_x, blue_bottom_right_y))
                blue_scoreboard_path = os.path.join(script_dir, "images\\blue_scoreboard.png")
                blue_crop.save(blue_scoreboard_path, format='PNG', optimize=False, compress_level=0, quality=100)
                # print(f"Blue scoreboard saved as: {blue_scoreboard_path}")
                # print(f"Blue crop coordinates: ({blue_top_left_x}, {blue_top_left_y}) to ({blue_bottom_right_x}, {blue_bottom_right_y})")
                
                # Run OCR processing if enabled
                if OCR:
                    print("\nOCR is enabled. Running get_scoreboard_value.py...")
                    try:
                        # Get the directory where this script is located
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        ocr_script_path = os.path.join(script_dir, "get_scoreboard_value.py")
                        
                        # Run the OCR script
                        result = subprocess.run([sys.executable, ocr_script_path], 
                                              capture_output=True, text=True, cwd=script_dir)
                        
                        if result.returncode == 0:
                            # print("Scoreboard OCR processing completed successfully!")
                            if result.stdout:
                                # print("OCR output:")
                                print(result.stdout)
                        else:
                            print("Scoreboard OCR processing failed!")
                            if result.stderr:
                                print("Error output:")
                                print(result.stderr)
                                
                    except Exception as ocr_error:
                        print(f"Error running scoreboard OCR script: {ocr_error}")
                else:
                    print("\nOCR is disabled. Skipping scoreboard OCR processing.")
                
            else:
                print("\nCannot create scoreboard crops - one or both score images not found")
                if not red_result:
                    print("  score_red.png not found")
                if not blue_result:
                    print("  score_blue.png not found")
                if OCR:
                    print("OCR is enabled but score images not found, skipping OCR processing.")
        else:
            print("Score image detection failed.")
        
        return filepath
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None

if __name__ == "__main__":
    # Play ready sound when program loads
    print("Program loaded. Playing ready notification...")
    try:
        import pygame
        pygame.mixer.init()
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ready_sound_path = os.path.join(script_dir, "sounds\\ready.mp3")
        pygame.mixer.music.load(ready_sound_path)
        pygame.mixer.music.play()
        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
    except Exception as sound_error:
        print(f"Could not play ready sound: {sound_error}")
    
    # Wait for TAB key press
    print("Press TAB key when you're ready to take a screenshot...")
    keyboard.wait('tab')
    
    # Make sure ProTanki is running and in full screen before executing this script
    print("Taking screenshot in 3 seconds...")
    time.sleep(0.2)  # Give you time to switch to the game window
    take_screenshot()