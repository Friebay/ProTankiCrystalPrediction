import cv2
import re
import requests
import numpy as np
import pandas as pd
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from io import BytesIO
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import time
import mss
import subprocess
import keyboard
import threading
import time
import winsound


# Define the path to the "Only_Screenshot_NoOutput.py" script
script_path = "Only_Screenshot_NoOutput.py"

# Define the key to trigger the script
trigger_key = ","

# Function to run the script
def run_script():
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the script. Error: {e}")

# Function to play sound
def play_sound():
    try:
        # Play a beep sound with frequency 1000Hz and duration 100ms
        winsound.Beep(1000, 100)
    except Exception as e:
        print(f"Failed to play sound. Error: {e}")

# Function to check for key events
def check_key_events():
    while True:
        if keyboard.is_pressed(trigger_key):  # Check if trigger key is held down
            play_sound()  # Play the sound
            run_script()  # Run the script
            time.sleep(0.5)  # Sleep to avoid repeated triggering
        else:
            time.sleep(0.1)  # Sleep for a short duration to avoid high CPU usage

# Create and start the key event checking thread
key_event_thread = threading.Thread(target=check_key_events)
key_event_thread.start()

# Keep the main thread running
while True:
    time.sleep(1)
