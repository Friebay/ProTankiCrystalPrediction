import pyautogui
import os
from datetime import datetime
import time
import keyboard
import cv2
import numpy as np
import subprocess
import sys

# OCR Toggle - Set to True to run OCR processing, False to skip it
OCR = True

def find_diamond_in_screenshot(screenshot_path):
    """Find diamond.png template in the screenshot and return its coordinates."""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, "images\\diamond.png")
        
        # Check if template exists
        if not os.path.exists(template_path):
            print(f"Template file not found: {template_path}")
            return None
        
        # Load the screenshot and template
        screenshot = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)
        
        if screenshot is None:
            print(f"Could not load screenshot: {screenshot_path}")
            return None
        
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
            
            # print(f"Diamond found at coordinates: ({center_x}, {center_y})")
            # print(f"Match confidence: {max_val:.3f}")
            # print(f"Top-left corner: {top_left}")
            # print(f"Bottom-right corner: ({top_left[0] + template_width}, {top_left[1] + template_height})")
            
            return {
                'center': (center_x, center_y),
                'top_left': top_left,
                'bottom_right': (top_left[0] + template_width, top_left[1] + template_height),
                'confidence': max_val
            }
        else:
            print(f"Diamond not found. Best match confidence: {max_val:.3f} (threshold: {threshold})")
            return None
            
    except Exception as e:
        print(f"Error finding diamond in screenshot: {e}")
        return None

def take_screenshot():
    """Take a screenshot of a specific region and save it in the script directory."""
    try:
        # Take a screenshot of the entire screen
        screenshot = pyautogui.screenshot()
        
        # Get screen width and height
        screen_width, screen_height = screenshot.size
        
        # Crop the image to the specified region (from x=1400 to right edge, y=1015 to bottom)
        cropped_screenshot = screenshot.crop((1400, 1015, screen_width, screen_height))
        
        # Generate a filename with timestamp
        filename = f"images\\protanki_screenshot.png"
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
        
        # Save the cropped screenshot
        cropped_screenshot.save(filepath, optimize=False, compress_level=0)
        
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
        except ImportError:
            print("pygame not installed. Trying alternative method...")
            try:
                import winsound
                # Use system default sound since winsound doesn't support MP3
                winsound.MessageBeep(winsound.MB_OK)
            except Exception as sound_error:
                print(f"Could not play sound: {sound_error}")
        except Exception as sound_error:
            print(f"Could not play sound: {sound_error}")
        
        print(f"Cropped screenshot saved as: {filepath}")
        
        # Find diamond in the screenshot
        print("Searching for diamond in the screenshot...")
        diamond_result = find_diamond_in_screenshot(filepath)
        
        if diamond_result:
            print("Diamond detection completed successfully!")
            
            # Crop around the diamond with specified margins
            diamond_center = diamond_result['center']
            print(f"Cropping around diamond at center: {diamond_center}")
            
            # Load the screenshot to crop around diamond
            screenshot_for_crop = pyautogui.screenshot()
            
            # Adjust coordinates relative to the original cropped area (add back the offset)
            original_crop_x = 1400
            original_crop_y = 1015
            
            # Calculate absolute coordinates on the full screen
            absolute_diamond_x = original_crop_x + diamond_center[0]
            absolute_diamond_y = original_crop_y + diamond_center[1]
            
            # Define crop margins
            crop_left = 100
            crop_up = 20
            crop_down = 30
            crop_right = 10
            
            # Calculate crop boundaries
            crop_x1 = max(0, absolute_diamond_x - crop_left)
            crop_y1 = max(0, absolute_diamond_y - crop_up)
            crop_x2 = min(screenshot_for_crop.width, absolute_diamond_x + crop_right)
            crop_y2 = min(screenshot_for_crop.height, absolute_diamond_y + crop_down)
            
            # Crop the image around the diamond
            battle_fund = screenshot_for_crop.crop((crop_x1, crop_y1, crop_x2, crop_y2))
            
            # Save the diamond-focused crop
            diamond_filename = f"images\\battle_fund.png"
            diamond_filepath = os.path.join(script_dir, diamond_filename)
            battle_fund.save(diamond_filepath, optimize=False, compress_level=0)
            
            print(f"Diamond-focused crop saved as: {diamond_filepath}")
            print(f"Crop dimensions: {crop_x2 - crop_x1} x {crop_y2 - crop_y1} pixels")
            print(f"Diamond position in original screen: ({absolute_diamond_x}, {absolute_diamond_y})")
            print(f"Crop boundaries: ({crop_x1}, {crop_y1}) to ({crop_x2}, {crop_y2})")
            
            # Run OCR processing if enabled
            if OCR:
                print("OCR is enabled. Running get_battle_fund_value.py...")
                try:
                    # Get the directory where this script is located
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    ocr_script_path = os.path.join(script_dir, "get_battle_fund_value.py")
                    
                    # Run the OCR script
                    result = subprocess.run([sys.executable, ocr_script_path], 
                                          capture_output=True, text=True, cwd=script_dir)
                    
                    if result.returncode == 0:
                        print("OCR processing completed successfully!")
                        if result.stdout:
                            print("OCR output:")
                            print(result.stdout)
                    else:
                        print("OCR processing failed!")
                        if result.stderr:
                            print("Error output:")
                            print(result.stderr)
                            
                except Exception as ocr_error:
                    print(f"Error running OCR script: {ocr_error}")
            else:
                print("OCR is disabled. Skipping OCR processing.")
            
        else:
            print("Diamond not found in the screenshot.")
            if OCR:
                print("OCR is enabled but diamond not found, skipping OCR processing.")
        
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
    except ImportError:
        print("pygame not installed. Trying alternative method...")
        try:
            import winsound
            # Use system default sound since winsound doesn't support MP3
            winsound.MessageBeep(winsound.MB_OK)
        except Exception as sound_error:
            print(f"Could not play ready sound: {sound_error}")
    except Exception as sound_error:
        print(f"Could not play ready sound: {sound_error}")
    
    # Wait for TAB key press
    print("Press TAB key when you're ready to take a screenshot...")
    keyboard.wait('tab')
    
    # Make sure ProTanki is running and in full screen before executing this script
    print("Taking screenshot in 3 seconds...")
    time.sleep(0.2)  # Give you time to switch to the game window
    take_screenshot()