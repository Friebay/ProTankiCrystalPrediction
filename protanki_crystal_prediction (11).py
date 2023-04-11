# -*- coding: utf-8 -*-
"""ProTanki Crystal Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13MFugR-YzQIVIC3_UdvyWEBiQQDFLDWm
"""

!sudo apt install tesseract-ocr
!pip install pytesseract

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import requests
from PIL import Image, ImageOps
import pytesseract
from io import BytesIO
import numpy as np


def create_dataset(data):
    X = data[:, 0].reshape(-1, 1)
    y = data[:, 1].reshape(-1, 1)
    return X, y

dataset1 = np.array([
    [1.020408163, 1.525445846],
    [1.049019608, 1.560103292],
    [1.086956522, 1.606557377],
    [1.148734177, 1.673073086],
    [1.162790698, 1.688362652],
    [1.166666667, 1.705882353],
    [1.192771084, 1.720207945],
    [1.25, 1.777794404],
    [1.25, 1.778464254],
    [1.283842795, 1.810702138],
    [1.333333333, 1.862068966],
    [1.363636364, 1.887345679],
    [1.388888889, 1.906616257],
    [1.388888889, 1.906961193],
    [1.4, 1.9218107],
    [1.416666667, 1.932327167],
    [1.428571429, 1.943669528],
    [1.45, 1.960015379],
    [1.485148515, 1.988570148],
    [1.5, 2.002361275]
])

X1, y1 = create_dataset(dataset1)

dataset2 = np.array([
    [1.485148515, 1.988570148],
    [1.5, 2.002361275],
    [1.8, 2.214345992],
    [1.851851852, 2.248992748],
    [1.886792453, 2.268008232],
    [1.930731707, 2.294513121],
    [2.040816327, 2.356053013],
    [2.25, 2.458695652],
    [2.5, 2.594771242],
    [2.729508197, 2.659179175],
    [3, 2.750310559],
    [3, 2.75708502],
    [3.125, 2.787451533],
    [3.333333333, 2.845689493],
    [3.511363636, 2.891874702],
    [4, 3.010186757],
    [4.666666667, 3.118362124],
    [5, 3.167769376],
    [5, 3.168224299],
    [5.479452055, 3.228808536],
    [5.800947867, 3.264898919],
    [5.941176471, 3.281713344],
    [6, 3.287804878],
    [6.301369863, 3.315228089],
    [7.5, 3.411666667],
    [7.5, 3.412280702],
    [8, 3.443908323]
])

X2, y2 = create_dataset(dataset2)

dataset3 = np.array([
    [8,3.443908323],
    [8.333333333,3.462385899],
    [8.5,3.474226804],
    [9.336448598,3.516258583],
    [10,3.55],
    [10,3.551210428],
    [11.11111111,3.586206897],
    [11.11111111,3.59112426],
    [12.33333333,3.6250295],
    [14,3.666483456],
    [14.27142857,3.672679505],
    [15.71428571,3.704481793],
    [16.66666667,3.720626632],
    [21.35714286,3.776863961],
    [22,3.782079165],
    [29,3.834249804],
    [30,3.83880597],
    [33.33333333,3.854470426],
    [34.44827586,3.858971552],
    [37.5,3.871282417],
    [50,3.902043932]
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

while True:
    Choosing = input("Enter 'hand' or 'image' to choose a program: ")

    if Choosing == 'Hand' or Choosing == 'hand':
        RedTeamScore = []

        while True:
            user_input = input("Red score ('0' or 'done' to finish): ")

            if user_input == 'done' or user_input == '0':
                break

            try:
                RedTeamScore.append(float(user_input))
            except ValueError:
                print("Invalid input. Please enter a number or 'done' to finish.")

        BlueTeamScore = []

        while True:
            user_input = input("Blue score ('0' or 'done' to finish): ")

            if user_input == 'done' or user_input == '0':
                break

            try:
                BlueTeamScore.append(float(user_input))
            except ValueError:
                print("Invalid input. Please enter a number or 'done' to finish.")
        break

    elif Choosing == 'Image' or Choosing == 'image':
        url = input("Enter a URL: ")

    response = requests.get(url)

    image = Image.open(BytesIO(response.content))

    width, height = image.size

    # Define the regions to crop
    #regions1 = [(911, 107, width - 963, height - 552), (0, 0, width, height)]
    #regions2 = [(911, 571, width - 963, height - 17), (0, 0, width, height)]

    # Extract the regions from the image
    #image1 = image.crop(regions1[0]).crop(regions1[1])
    #image2 = image.crop(regions2[0]).crop(regions2[1])

    #image1 = image.crop(regions1[0])
    #image2 = image.crop(regions2[0])

    # Save cropped images
    #image1.save("RedCroppedScore.png")
    #image2.save("BlueCroppedScore.png")

    # Resize and process cropped images
    #resized_image1 = image1.resize((image1.width * 1, image1.height * 1))
    #resized_image2 = image2.resize((image2.width * 1, image2.height * 1))

    #bw_image1 = ImageOps.invert(resized_image1.convert('RGB')).convert('L')
    #bw_image2 = ImageOps.invert(resized_image2.convert('RGB')).convert('L')

    #bw_image1.save("RedBW.png")
    #bw_image2.save("BlueBW.png")

    # Extract scores using Tesseract
    xconfig = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
    #text1 = pytesseract.image_to_string(bw_image1, config=xconfig)
    #text2 = pytesseract.image_to_string(bw_image2, config=xconfig)

    #red_score = list(map(int, text1.strip().split()))
    #blue_score = list(map(int, text2.strip().split()))

    # Store scores in a list
    #scores = [red_score, blue_score]

    break

else:
      print("Invalid input. Please enter 'Hand' or 'Image'.")

xconfig = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'

url = input("Enter a URL: ")

response = requests.get(url)

from PIL import Image, ImageOps
import pytesseract
import cv2
from google.colab.patches import cv2_imshow

# Open the image
image = Image.open(BytesIO(response.content))

# Get the width and height of the image
width, height = image.size

# Define the region to be cropped (1500 pixels from the left, 1040 pixels from the top, 200 pixels from the right)
region = (1500, 1035, width - 150, height - 22)

# Crop the image to the specified region
cropped_image = image.crop(region)

# Save the cropped image
cropped_image.save('fund.png')

# Resize the cropped image
resized_image = cropped_image.resize((cropped_image.width * 8, cropped_image.height * 6))

# Convert the resized image to black and white
bw_image = ImageOps.invert(resized_image.convert('RGB')).convert('L')

# Save the black and white image
bw_image.save("fund_BW.png")

image = cv2.imread('fund_BW.png', 0)
thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# Perform text extraction
results = pytesseract.image_to_data(thresh, lang='eng', output_type='dict', config='--psm 10')

# Find the word "Battle" in the results and get its coordinates
word_x, word_y, word_w, word_h = None, None, None, None
for idx, text in enumerate(results['text']):
    if text == 'Battle':
        word_x = results['left'][idx]
        word_y = results['top'][idx]
        word_w = results['width'][idx]
        word_h = results['height'][idx]
        break

if word_x is not None:
    # Define the region of interest (ROI) around the word "Battle"
    roi = (word_x + 530, word_y, word_w + 540, word_h)

    # Crop the thresholded image to the ROI
    cropped_word = thresh[word_y:word_y + word_h, word_x + 530:word_x + word_w + 540]

    # Save the cropped word as a new image
    cv2.imwrite('battle.png', cropped_word)

    # Show the cropped word
    cv2_imshow(cropped_word)

    print("The word 'Battle' has been cropped and saved as 'battle.png'.")
else:
    print("The word 'Battle' was not found in the image.")

# Use Tesseract to recognize text from the image
fund = pytesseract.image_to_string('battle.png', config=xconfig)
funds = list(map(int, fund.strip().split()))

funds

from PIL import Image, ImageOps
import pytesseract
import re
from google.colab.patches import cv2_imshow

# Open the image
image = Image.open(BytesIO(response.content))

# Get the width and height of the image
width, height = image.size

# Define the region to be cropped (1500 pixels from the left, 1027 pixels from the top, 200 pixels from the right)
region = (1770, 1030, width-10, height-15)

# Crop the image to the specified region
cropped_image = image.crop(region)

# Save the cropped image
cropped_image.save('flags.png')

# Resize the cropped image
resized_image = cropped_image.resize((cropped_image.width * 8, cropped_image.height * 6))

# Convert the resized image to black and white
bw_image = ImageOps.invert(resized_image.convert('RGB')).convert('L')

# Save the black and white image
bw_image.save("flags_BW.png")

image = cv2.imread('flags_BW.png', 0)
thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Use Tesseract to recognize text from the image
flag = pytesseract.image_to_string(thresh, config='--psm 9')

# Remove non-numeric characters from the recognized text
flags = re.findall(r'\d+', flag)

# Convert the recognized numbers to integers
flags = list(map(int, flags))

print(flag)
print(flags)
cv2_imshow(thresh)

from PIL import Image, ImageOps
import pytesseract
import re
from google.colab.patches import cv2_imshow

# Open the image
image = Image.open(BytesIO(response.content))

# Get the width and height of the image
width, height = image.size

# Define the region to be cropped (1500 pixels from the left, 1027 pixels from the top, 200 pixels from the right)
region = (920, 150, width - 950, height-98)

# Crop the image to the specified region
cropped_image = image.crop(region)

# Save the cropped image
cropped_image.save('full_score.png')

# Resize the cropped image
resized_image = cropped_image.resize((cropped_image.width * 3, cropped_image.height * 3))

# Convert the resized image to black and white
bw_image = ImageOps.invert(resized_image.convert('RGB')).convert('L')

# Save the black and white image
bw_image.save("full_score_BW.png")

image = cv2.imread('full_score_BW.png', 0)
thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Use Tesseract to recognize text from the image
score = pytesseract.image_to_string(thresh, config=xconfig)
scores = list(map(int, score.strip().split()))

if scores[0] < scores[1]:
    # Remove the first number from the list
    scores.pop(0)

original_list = scores

if original_list[0] < original_list[1]:
    # Remove the first number from the list
    original_list.pop(0)

# Split the list in the middle when previous number is smaller than the following number
for i in range(1, len(original_list)):
    if original_list[i - 1] < original_list[i]:
        left_list = original_list[:i]
        right_list = original_list[i:]
        break

for i in range(len(right_list)-1, 0, -1):
    if right_list[i] >= right_list[i-1]:  # Compare current element with previous element
        right_list.pop(i)  # Remove the current element if it's not smaller

print(scores)
print("Left list:", left_list)
print("Right list:", right_list)

# Display the thresh image
cv2_imshow(thresh)

print(funds)
print(flags)
print(left_list)
print(right_list)

RedFlag = int(input("Red flag amount: "))
BlueFlag = int(input("Blue flag amount: "))

BattleFund = int(input("Enter the BattleFund amount: "))
print('\n')

WinningScore = []
LossingScore = []

if RedFlag>BlueFlag:
  WinningFlag=RedFlag
  LossingFlag=BlueFlag
  if(Choosing == 'Hand' or Choosing == 'hand'):
    WinningScore=RedTeamScore
    LossingScore=BlueTeamScore
  else:
    WinningScore=scores[1]
    LossingScore=scores[0]
else:
  WinningFlag=BlueFlag
  LossingFlag=RedFlag
  if(Choosing == 'Hand' or Choosing == 'hand'):
    WinningScore=BlueTeamScore
    LossingScore=RedTeamScore
  else:
    WinningScore=scores[0]
    LossingScore=scores[1]

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

if RedFlag > BlueFlag:
    print('Red Team players will get: ', ', '.join(map(str, WinningIndividualCrystals)))
    print('\n')
    print('Blue Team players will get: ', ', '.join(map(str, LossingIndividualCrystals)))
else:
    print('Red Team players will get: ', ', '.join(map(str, LossingIndividualCrystals)))
    print('\n')
    print('Blue Team players will get: ', ', '.join(map(str, WinningIndividualCrystals)))

import time
time.sleep(60000)