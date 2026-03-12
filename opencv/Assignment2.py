import cv2
loc= input("What is the location of the image? ")
image=cv2.imread(loc)
if image is None:
    print("Image Not Found")
    exit()

wish=input("What do you want ? Line/Circle/ Rectangle/ Text ? ")
if wish == "Line":
    pt1=(int(input("Enter Pointer One: x= ")),int(input("Enter Pointer One: y= ")))
    pt2=(int(input("Enter Pointer Two: x= ")),int(input("Enter Pointer Two: y= ")))
    cv2.line(image,pt1,pt2,(255,0,0),2)


elif wish == "Rectangle":
    pt1 = (int(input("Enter Pointer One: x= ")), int(input("Enter Pointer One: y= ")))
    pt2 = (int(input("Enter Pointer Two: x= ")), int(input("Enter Pointer Two: y= ")))
    cv2.rectangle(image,pt1,pt2,(255,0,0),2)

elif wish == "Circle":
    center=(int(input("Enter Center's: x= ")), int(input("Enter Center's: y= ")))
    radius=int(input("Enter the radius of circle: "))
    cv2.circle(image,center,radius,(255,0,0),2)

elif wish == "Text" :
    text=input("Enter Text: ")
    origin= (int(input("Enter Origin: x= ")), int(input("Enter Origin: y= ")))
    cv2.putText(image,text,origin,cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

else :
    print("Invalid Input")
    exit()

save=input("Do you want to save the image?Y/N: ")
if save == "Y" :
    cv2.imwrite("Save.png",image)

cv2.imshow("Image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()





