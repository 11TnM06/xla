import cv2
import imutils
import numpy as np

img1 = cv2.imread("./images/challenge1_1.png")
img1 = cv2.resize(img1, (550, 360))

img2 = cv2.imread("./images/challenge1_2.png")
img2 = cv2.resize(img2, (550, 360))

# Grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# Find the difference between the two images
diff = cv2.absdiff(gray1, gray2)

# Show
#cv2.imshow("diff(img1, img2)", diff)
# cv2.imshow("Original Picture", img1)
# cv2.imshow("Modified Picture", img2)

# Threshold the difference image, followed by finding contours to
threshold = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imshow("Threshold", threshold)
# Dilitation
kernel = np.ones((5,5), np.uint8)
dilation = cv2.dilate(threshold, kernel, iterations = 1)
cv2.imshow("Dilation", dilation)
# Contours
countours = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
countours = imutils.grab_contours(countours)
for countour in countours:
    if cv2.contourArea(countour) <= 100:
        continue
    x, y, w, h = cv2.boundingRect(countour)
    cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

x = np.zeros((360, 10, 3), np.uint8)
result = np.hstack((img1, x, img2))
cv2.imshow("Difference", result)
cv2.waitKey()
cv2.destroyAllWindows()


