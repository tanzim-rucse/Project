import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # Draw face rectangle
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(frame,"Face",(x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray,1.1,8)

        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        if len(eyes) > 0:
            cv2.putText(frame,"Eyes Detected",(x,y-30),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

        # Detect smile (lower half of face)
        smile_roi_gray = roi_gray[int(h/2):h, :]
        smile_roi_color = roi_color[int(h/2):h, :]

        smiles = smile_cascade.detectMultiScale(smile_roi_gray,1.7,22)

        for (sx,sy,sw,sh) in smiles:
            cv2.rectangle(smile_roi_color,(sx,sy),(sx+sw,sy+sh),(0,0,255),2)
            cv2.putText(frame,"Smiling",(x,y+h+20),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            break

    cv2.imshow("Face Eye Smile Detection",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()