import cv2

image = cv2.imread("Pasted_image.png")

if image is None:
    print("Nothing")

else: 
    print("YES")    