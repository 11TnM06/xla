import cv2
import numpy as np
from skimage.metrics import structural_similarity
img1 = cv2.imread("./images/city1.jpg")
img1 = cv2.resize(img1, (600, 360))
img2 = cv2.imread("./images/city2.jpg")
img2 = cv2.resize(img2, (600, 360))

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

(score, diff) = structural_similarity(gray1, gray2, full=True)
diff = (diff * 255).astype("uint8")

_, threshold = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]


for contour in contours:
    if cv2.contourArea(contour) <= 80:
        continue
    (x, y, w, h) = cv2.boundingRect(contour)
    #cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("Orginal", img1)
cv2.imshow("Modified", img2)
cv2.waitKey()
cv2.destroyAllWindows()



