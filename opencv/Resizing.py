import cv2
image = cv2.imread("PXL_20250820_162110955.PORTRAIT.jpg")
if image is None:
    print("Image Not Found")
else:
    resized_image = cv2.resize(image,(300,300))
    cv2.imshow("Original",image)
    cv2.imshow("Resized Image",resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("Resized_image.jpg",resized_image)
