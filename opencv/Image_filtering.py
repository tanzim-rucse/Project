import cv2
import numpy as np

image = cv2.imread("Tazim.png")
"""
blurred_image= cv2.GaussianBlur(image,(5,5),1)

kernal=np.array([
    [0,-1,0],
    [-1,5,-1],
    [0,-1,0]
])
sharped_photo=cv2.filter2D(image,5,kernal)

sharped_photo = cv2.medianBlur(image,5)

edges=cv2.Canny(image,150,200)
 """
circle_ph= cv2.circle(image,(150,150),100,(255,0,0),-1)
rectengle_ph=cv2.rectangle(image,(100,100),(250,250),(255,0,0),-1)

bitwise_and= cv2.bitwise_and(circle_ph,rectengle_ph)
bitwise_or=cv2.bitwise_or(circle_ph,rectengle_ph)
bitwise_not= cv2.bitwise_not(circle_ph)


cv2.imshow("Original", image)
cv2.imshow("And", bitwise_and)
cv2.imshow("Or", bitwise_or)
cv2.imshow("Not", bitwise_not)

cv2.waitKey(0)
cv2.destroyAllWindows()

