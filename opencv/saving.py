import cv2
image = cv2.imread("Pasted_image.png")
if image is not None:
    success=cv2.imwrite("Output.png",image)
    if success:
        print("Image saved")
    else:
        print("Image NOT saved")
else:
    print("Error")
