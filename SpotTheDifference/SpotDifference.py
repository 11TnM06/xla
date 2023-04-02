import cv2
import imutils
import numpy as np

img1 = cv2.imread("../GameData/image/result_images/original_image.jpg")
img1 = cv2.resize(img1, (600, 360))
img2 = cv2.imread("../GameData/image/result_images/converted_image.jpg")
img2 = cv2.resize(img2, (600, 360))
img_height = img1.shape[0]

# Grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Find the difference between the two images
diff = cv2.absdiff(gray1, gray2)
#cv2.imshow("Difference", diff)

# Threshold the difference image, followed by finding contours to
threshold = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#cv2.imshow("Threshold", threshold)

# Dilation
kernel = np.ones((5,5), np.uint8) 
dilate = cv2.dilate(threshold, kernel, iterations=2) 
#cv2.imshow("Dilate", dilate)

# Contours
countours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
countours = imutils.grab_contours(countours)
for countour in countours:
    if cv2.contourArea(countour) <= 100:
        continue

    #circle
    (x, y), radius = cv2.minEnclosingCircle(countour)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(img2, center, radius, (0, 255, 0), 2)
    
x = np.zeros((img_height, 10, 3), np.uint8)
result = np.hstack((img1, x, img2))
cv2.imshow("Difference", result)
cv2.waitKey()
cv2.destroyAllWindows()


