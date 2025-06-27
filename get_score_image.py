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

def take_screenshot():
    """Take a screenshot of a specific region and save it in the script directory."""
    try:
        # Take a screenshot of the entire screen
        screenshot = pyautogui.screenshot()

        # Crop the image to the specified region (from x=1700 to right edge, y=1025 to bottom)
        cropped_screenshot = screenshot.crop((1700, 1025, 1900, 1055))
        
        filename = f"images\\flag_crop.png"
        
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
        except Exception as sound_error:
            print(f"Could not play sound: {sound_error}")
        
        print(f"Cropped screenshot saved as: {filepath}")
        
        # Run OCR processing if enabled
        if OCR:
            print("OCR is enabled. Running get_score_value.py...")
            try:
                # Get the directory where this script is located
                script_dir = os.path.dirname(os.path.abspath(__file__))
                ocr_script_path = os.path.join(script_dir, "get_score_value.py")
                
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