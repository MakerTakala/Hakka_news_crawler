import cv2
import numpy as np
import pytesseract

img = cv2.imread('test_data/sample2.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 0, 0), (360, 8, 255))
mask = cv2.bitwise_not(mask)
img[np.where(mask)] = 0
img = cv2.bitwise_not(img)

img[np.where((img >= [128, 128, 128]).all(axis=2))] = [255, 255, 255]

# do threshold use otsu's algorithm
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
img = cv2.bitwise_not(thresh)

cv2.imwrite('test_data/result.png', img)

# run tesseract, returning
boxes = pytesseract.image_to_string(img, lang='chi_tra', config="--psm 7")
print(boxes)
