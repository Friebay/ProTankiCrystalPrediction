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

pytesseract.pytesseract.tesseract_cmd = r'OCR\tesseract.exe'

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

time.sleep(5)

image = Image.open("Screenshot.png")

width, height = image.size

region = (1500, 1035, width - 150, height - 20)

cropped_image = image.crop(region)

cropped_image.save('fund.png')

resized_image = cropped_image.resize((cropped_image.width * 8, cropped_image.height * 5))

bw_image = ImageOps.invert(resized_image.convert('RGB')).convert('L')

bw_image.save("fund_BW.png")

image = cv2.imread('fund_BW.png', 0)

image = cv2.GaussianBlur(image, (3, 3), 0)

kernel = np.array([[-1, -1, -1],
                   [-1,  9, -1],
                   [-1, -1, -1]])

image_sharpened = cv2.filter2D(image, -1, kernel)

_, thresh = cv2.threshold(image_sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

results = pytesseract.image_to_data(thresh, lang='eng', output_type='dict', config='--psm 10')

word_x, word_y, word_w, word_h = None, None, None, None
for idx, text in enumerate(results['text']):
    if text == 'Battle':
        word_x = results['left'][idx]
        word_y = results['top'][idx]
        word_w = results['width'][idx]
        word_h = results['height'][idx]
        break

if word_x is not None:
    roi = (word_x + 510, word_y, word_w + 540, word_h)

    cropped_word = thresh[word_y:word_y + word_h, word_x + 510:word_x + word_w + 540]

    cv2.imwrite('battle.png', cropped_word)

    print("The word 'Battle' has been cropped and saved as 'battle.png'.")
else:
    print("The word 'Battle' was not found in the image.")

fund = pytesseract.image_to_string('battle.png', config=xconfig)
funds = list(map(int, fund.strip().split()))

image = Image.open("Screenshot.png")

width, height = image.size

region = (1770, 1030, width-10, height-15)

cropped_image = image.crop(region)

cropped_image.save('flags.png')

resized_image = cropped_image.resize((cropped_image.width * 6, cropped_image.height * 4))

bw_image = ImageOps.invert(resized_image.convert('RGB')).convert('L')

bw_image.save("flags_BW.png")

image1 = Image.open("flags_BW.png")

kernel = ImageFilter.Kernel((3, 3), [0, -1, 0, -1, 5, -1, 0, -1, 0])

sharp_image = image1.filter(kernel)

sharp_image.save("flagSHARP.png")

image = cv2.imread('flagSHARP.png', 0)

thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

flag = pytesseract.image_to_string(thresh, config='--psm 10')

flags = re.findall(r'\d+', flag)

flags = list(map(int, flags))


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


if scores[0] < scores[1]:
    scores.pop(0)

original_list = scores

if original_list[0] < original_list[1]:
    original_list.pop(0)

for i in range(1, len(original_list)):
    if original_list[i - 1] < original_list[i]:
        left_list = original_list[:i]
        right_list = original_list[i:]
        break

for i in range(len(right_list)-1, 0, -1):
    if right_list[i] >= right_list[i-1]:
        right_list.pop(i)



BlueFlag = flags[-1]

RedFlag = flags[-2]

RedTeamScore=left_list
BlueTeamScore=right_list

BattleFund = int(funds[0])

WinningScore = []
LossingScore = []

print("Fund:", BattleFund)
print("Red score:", RedTeamScore)
print("Blue score:", BlueTeamScore)
print("Red flag:", RedFlag)
print("Blue flag:", BlueFlag)


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

# Print the team players' crystals based on RedFlag and BlueFlag
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

time.sleep(20)

