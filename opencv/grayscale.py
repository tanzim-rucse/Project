import cv2
image=cv2.imread("Pasted_image.png")
if image is not None:
    gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale",gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Can't find any image")