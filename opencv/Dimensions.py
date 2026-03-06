import cv2
image =cv2.imread("Pasted_image.png")
if image is not None:
    h=image.shape[0]
    w=image.shape[1]
    c=image.shape[2]
    print("Image loaded")
    print("Height:",h)
    print("Width:",w)
    print("Channels:",c)

else:
    print("Image not loaded")