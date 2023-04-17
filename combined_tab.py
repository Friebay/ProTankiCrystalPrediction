import cv2
import re
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import time
import mss
import keyboard
import threading
import winsound
import tkinter as tk
import os

# OCR location. Since it's in the same location as the code, we use this kind of location thing
pytesseract.pytesseract.tesseract_cmd = r'OCR\tesseract.exe'

def display_results(RedFlag, BlueFlag, WinningResult, LossingResult, BattleFund):
    # Create a tkinter window
    root = tk.Tk()
    root.title("Results")

    # Set the window to be transparent
    root.attributes('-alpha', 0.7)  # Set the alpha value to control transparency (0.0 to 1.0)

    # Set the window to be always on top
    root.attributes('-topmost', True)

    # Set the window to not have any decorations (title bar, etc.)
    root.overrideredirect(True)

    # Set the window size and position
    window_width = 100
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = 0  # on the left side
    y = (screen_height - window_height) // 2 # in the middle
    root.geometry(f"{window_width}x{window_height}+{x}+{y}") # Set the window geometry based on window_width, window_height, x, and y values.

    # Create a tkinter text widget to display the results text
    text_widget = tk.Text(root, font=("Arial", 10), fg="white", bg="black")
    text_widget.pack(expand=True, fill=tk.BOTH) # Pack the text_widget to fill both horizontally and vertically in the parent widget, allowing it to expand as needed.

    # Convert the numerical values to strings
    red_flag_str = "Red Flag: " + str(RedFlag)
    blue_flag_str = "Blue Flag: " + str(BlueFlag)
    fund_str = "Fund: " + str(BattleFund)

    # Insert the strings into the text widget
    text_widget.insert(tk.END, f"{red_flag_str}\n{blue_flag_str}\n{fund_str}")


    # Insert the results text into the text widget
    if RedFlag > BlueFlag:
        text_widget.insert(tk.END, "\nRed:\n")
        text_widget.insert(tk.END, '\n'.join(map(str, WinningResult)) + '\n')
        text_widget.insert(tk.END, "Blue:\n")
        text_widget.insert(tk.END, '\n'.join(map(str, LossingResult)) + '\n')
    else:
        text_widget.insert(tk.END, "\nRed:\n")
        text_widget.insert(tk.END, '\n'.join(map(str, LossingResult)) + '\n')
        text_widget.insert(tk.END, "Blue:\n")
        text_widget.insert(tk.END, '\n'.join(map(str, WinningResult)) + '\n')

    # Function to close the window when clicked
    def close_window(event):
        root.destroy()

    # Bind a mouse click event to close the window
    text_widget.bind("<Button-1>", close_window)

    # Start tkinter event loop
    root.mainloop()

def run_script():
        # List of file paths to delete
    files_to_delete = [
        "battle.png",
        "flags.png",
        "flags_BW.png",
        "flagsSHARP.png",
        "full_score.png",
        "full_score_BW.png",
        "full_score_SHARP.png",
        "fund.png",
        "fund_BW.png",
        "screenshot.png"
    ]

    # Loop through the list of files and attempt to remove each one
    for file_path in files_to_delete:
        # Check if the file exists
        if os.path.exists(file_path):
            # Attempt to remove the file
            try:
                os.remove(file_path)
            except Exception as e:
                pass
        else:
            pass
    
    
        def create_dataset(data):
            X = data[:, 0].reshape(-1, 1)
            y = data[:, 1].reshape(-1, 1)
            return X, y

        dataset1 = np.array([
        [1.020, 1.525],
        [1.049, 1.560],
        [1.087, 1.607],
        [1.149, 1.673],
        [1.163, 1.688],
        [1.167, 1.706],
        [1.193, 1.720],
        [1.250, 1.778],
        [1.250, 1.778],
        [1.284, 1.811],
        [1.333, 1.862],
        [1.364, 1.887],
        [1.389, 1.907],
        [1.389, 1.907],
        [1.400, 1.922],
        [1.417, 1.932],
        [1.429, 1.944],
        [1.450, 1.960],
        [1.485, 1.989],
        [1.500, 2.002]
    ])

        X1, y1 = create_dataset(dataset1)

        dataset2 = np.array([
        [1.485, 1.989],
        [1.500, 2.002],
        [1.800, 2.214],
        [1.852, 2.249],
        [1.887, 2.268],
        [1.931, 2.295],
        [2.041, 2.356],
        [2.250, 2.459],
        [2.500, 2.595],
        [2.730, 2.659],
        [3.000, 2.750],
        [3.000, 2.757],
        [3.125, 2.787],
        [3.333, 2.846],
        [3.511, 2.892],
        [4.000, 3.010],
        [4.667, 3.118],
        [5.000, 3.168],
        [5.000, 3.168],
        [5.479, 3.229],
        [5.801, 3.265],
        [5.941, 3.282],
        [6.000, 3.288],
        [6.301, 3.315],
        [7.500, 3.412],
        [7.500, 3.412],
        [8.000, 3.444]
    ])

        X2, y2 = create_dataset(dataset2)

        dataset3 = np.array([
        [8.000, 3.444],
        [8.333, 3.462],
        [8.500, 3.474],
        [9.336, 3.516],
        [10.000, 3.550],
        [10.000, 3.551],
        [11.111, 3.586],
        [11.111, 3.591],
        [12.333, 3.625],
        [14.000, 3.666],
        [14.271, 3.673],
        [15.714, 3.704],
        [16.667, 3.721],
        [21.357, 3.777],
        [22.000, 3.782],
        [29.000, 3.834],
        [30.000, 3.839],
        [33.333, 3.854],
        [34.448, 3.859],
        [37.500, 3.871],
        [50.000, 3.902]
    ])

        X3, y3 = create_dataset(dataset3)

        poly_reg1 = PolynomialFeatures(degree=3)
        X_poly1 = poly_reg1.fit_transform(X1)

        poly_reg2 = PolynomialFeatures(degree=5)
        X_poly2 = poly_reg2.fit_transform(X2)

        poly_reg3 = PolynomialFeatures(degree=5)
        X_poly3 = poly_reg3.fit_transform(X3)

        pol_reg1 = LinearRegression()
        pol_reg2 = LinearRegression()
        pol_reg3 = LinearRegression()

        pol_reg1.fit(X_poly1, y1)
        pol_reg2.fit(X_poly2, y2)
        pol_reg3.fit(X_poly3, y3)
        
        #wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww

        xconfig = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'

        def capture_screenshot():
            with mss.mss() as sct:
                # Set monitor coordinates for full screen
                monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

                # Get raw pixels from the screen, save it to a Numpy array
                img = np.array(sct.grab(monitor))

                # Save the screenshot to a file
                cv2.imwrite("screenshot.png", img)
                print("Screenshot saved!")

        capture_screenshot()
        
        #wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww

        # Open image
        image = Image.open("Screenshot.png")

        # Get image size
        width, height = image.size

        # Crop image
        region = (1490, 1033, width - 150, height - 18)
        cropped_image = image.crop(region)

        # Save cropped image
        cropped_image.save('fund.png')

        # Resize cropped image
        resized_image = cropped_image.resize((cropped_image.width * 8, cropped_image.height * 7))

        # Invert colors and convert to grayscale
        bw_image = ImageOps.invert(resized_image.convert('RGB')).convert('L')

        # Save black and white image
        bw_image.save("fund_BW.png")

        # Read image using OpenCV
        image = cv2.imread('fund_BW.png', 0)

        # Apply Gaussian blur
        image = cv2.GaussianBlur(image, (3, 3), 0)

        # Define sharpening kernel
        kernel = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
        
        # Apply sharpening filter
        image_sharpened = cv2.filter2D(image, -1, kernel)

        # Apply Otsu's thresholding
        _, thresh = cv2.threshold(image_sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform OCR using Tesseract
        results = pytesseract.image_to_data(thresh, lang='eng', output_type='dict', config='--psm 10')
        
        print(results)
                
        # The main issue of this whole code is that pytesseract doesn't find the word "Battle" so I added this little code to make sure that the word "Battle" is indeed in the cropped picture
        #cv2.imshow('Window Name', thresh)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        word_x, word_y, word_w, word_h = None, None, None, None # Trying to get "Battle" coordinates
        for idx, text in enumerate(results['text']):
            if text in ['Battle', 'wattle', 'bottle', 'battle', 'satte', 'sattle', 'cattle', 'attic', 'atte', 'seattle', 'pattie']:
                word_x = results['left'][idx]
                word_y = results['top'][idx]
                word_w = results['width'][idx]
                word_h = results['height'][idx]
                break

        if word_x is not None:
            # Move to the right of the word "Battle" so that only the fund would be visable
            roi = (word_x + 475, word_y, word_w + 540, word_h)

            cropped_word = thresh[word_y:word_y + word_h, word_x + 510:word_x + word_w + 540]

            cv2.imwrite('battle.png', cropped_word)

            print("The word 'Battle' has been cropped and saved as 'battle.png'.")
        else:
            print("The word 'Battle' was not found in the image.")

        fund = pytesseract.image_to_string('battle.png', config=xconfig)# OCRing "Battle fund" numbers
        funds = list(map(int, fund.strip().split()))

        # Almost the same as above
        image = Image.open("Screenshot.png")
        width, height = image.size
        region = (1770, 1030, width-10, height-15)
        cropped_image = image.crop(region)
        cropped_image.save('flags.png')
        resized_image = cropped_image.resize((cropped_image.width * 6, cropped_image.height * 4))
        bw_image = ImageOps.invert(resized_image.convert('RGB')).convert('L')
        bw_image.save("flags_BW.png")
        image1 = Image.open("flags_BW.png")
        kernel = ImageFilter.Kernel((3, 3), [0, -1, 0, -1, 5, -1, 0, -1, 0])#sharpening
        sharp_image = image1.filter(kernel)#applying sharpening
        sharp_image.save("flagSHARP.png")
        image = cv2.imread('flagSHARP.png', 0)
        thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]# black and white, a lot of exposure so that text is clearly seen
        flag = pytesseract.image_to_string(thresh, config='--psm 10') #OCRing flag numbers
        flags = re.findall(r'\d+', flag)
        flags = list(map(int, flags))
        
        # Almost the same as above
        image = Image.open("Screenshot.png")
        width, height = image.size
        region = (920, 150, width - 950, height - 98)
        cropped_image = image.crop(region)
        cropped_image.save('full_score.png')
        resized_image = cropped_image.resize((cropped_image.width * 4, cropped_image.height * 3))
        bw_image = ImageOps.invert(resized_image.convert('RGB')).convert('L')
        bw_image.save("full_score_BW.png")
        kernel = ImageFilter.Kernel((3, 3), [0, -1, 0, -1, 5, -1, 0, -1, 0])
        sharp_image = bw_image.filter(kernel)
        sharp_image.save("full_score_SHARP.png")
        image = cv2.cvtColor(np.array(sharp_image), cv2.COLOR_GRAY2BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        score = pytesseract.image_to_string(thresh, config=xconfig)
        scores = list(map(int, score.strip().split()))

        print(33333333333333333333333333)
        
        # Check if the first element is smaller than the second element, remove if necessary
        if scores[0] < scores[1]:
            scores.pop(0)

        # Create a copy of the original list
        original_list = scores.copy()

        # Check if the first element of the copied list is smaller than the second element, remove if necessary
        if original_list[0] < original_list[1]:
            original_list.pop(0)

        # Divide the scores into two teams by finding where one number is bigger than the previous one
        for i in range(1, len(original_list)):
            if original_list[i - 1] < original_list[i]:
                left_list = original_list[:i]
                right_list = original_list[i:]
                break

        # Remove elements from right_list that are greater than or equal to the element immediately before them
        for i in range(len(right_list)-1, 0, -1):
            if right_list[i] >= right_list[i-1]:
                right_list.pop(i)
                
        # Remove elements from right_list that are greater than or equal to the element immediately before them
        for i in range(len(right_list)-1, 0, -1):
            if left_list[i] >= left_list[i-1]:
                left_list.pop(i)

        #wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
        
        # Some bug here
        print(444444444444444444444444)
        
        print(flag)

        BlueFlag = flags[-1]
        print(555555555555555555555)
        RedFlag = flags[-2]
        
        #wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
        
        RedTeamScore=left_list
        BlueTeamScore=right_list
        
        BattleFund = int(funds[0])
        
        WinningScore = []
        LossingScore = []
        
        print()
        print("Fund:", BattleFund)
        print("Red score:", RedTeamScore)
        print("Blue score:", BlueTeamScore)
        print("Red flag:", RedFlag)
        print("Blue flag:", BlueFlag)
        print()

        if RedFlag>BlueFlag:
            WinningFlag=RedFlag
            LossingFlag=BlueFlag
            WinningScore=RedTeamScore
            LossingScore=BlueTeamScore
        else:
            WinningFlag=BlueFlag
            LossingFlag=RedFlag
            WinningScore=BlueTeamScore
            LossingScore=RedTeamScore

        if RedFlag == BlueFlag:
            PredictionRatio = 1
        elif LossingFlag == 0:
            PredictionRatio = 4
        else:
            FlagRatio = WinningFlag / LossingFlag
            if FlagRatio < 1.5:
                PredictionRatio = pol_reg1.predict(poly_reg1.fit_transform([[FlagRatio]]))
            elif FlagRatio > 8:
                PredictionRatio = pol_reg3.predict(poly_reg3.fit_transform([[FlagRatio]]))
            else:
                PredictionRatio = pol_reg2.predict(poly_reg2.fit_transform([[FlagRatio]]))

        LossingTeamCrystals = BattleFund * (1 / (PredictionRatio + 1))
        WinningTeamCrystals = BattleFund - LossingTeamCrystals

        WinningCrystal = WinningTeamCrystals / sum(WinningScore)
        LossingCrystal = LossingTeamCrystals / sum(LossingScore)

        WinningIndividualCrystals = np.round(np.multiply(WinningScore, WinningCrystal), 0)
        LossingIndividualCrystals = np.round(np.multiply(LossingScore, LossingCrystal), 0)

        WinningIndividualCrystals = np.array(WinningIndividualCrystals)
        LossingIndividualCrystals = np.array(LossingIndividualCrystals)

        # Concatenate the arrays horizontally
        WinningResult = np.column_stack(WinningIndividualCrystals)
        LossingResult = np.column_stack(LossingIndividualCrystals)
        
        display_results(RedFlag, BlueFlag, WinningResult, LossingResult, BattleFund)
        
        # Print the team players crystals
        if RedFlag > BlueFlag:
            print('Red Team players will get:')
            print('\n'.join(map(str, WinningResult)))
            print('\nBlue Team players will get:')
            print('\n'.join(map(str, LossingResult)))
        else:
            print('Red Team players will get:')
            print('\n'.join(map(str, LossingResult)))
            print('\nBlue Team players will get:')
            print('\n'.join(map(str, WinningResult)))

def play_sound():
    try:
        # Play a beep sound
        winsound.Beep(1000, 100)
    except Exception as e:
        print(f"Failed to play sound. Error: {e}")

# Function to check for key events
def check_key_events():
    while True:
        try:
            if keyboard.is_pressed("tab"):  # Check if trigger key is held down
                play_sound()  # Play the sound
                run_script()  # Run the script
                time.sleep(7)  # Sleep to avoid repeated triggering
            else:
                # Sleep for a short duration to avoid high CPU usage
                time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")  # Print the error message
            continue  # Continue to the next iteration of the loop

# Create and start the key event checking thread
key_event_thread = threading.Thread(target=check_key_events)
key_event_thread.start()
time.sleep(2)

# Keep the main thread running
while True:
    time.sleep(1)