import cv2
location= input("Enter the location of Image: ")
image=cv2.imread(location)
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ask=input("Show / Save? : ")
if ask=="Show":
    if gray is not None:
        cv2.imshow("Image of Gray: ",gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Image not available")
else:
    name= input("What is the name of the image? ")
    cv2.imwrite(name,gray)
    print("Image saved successfully")
