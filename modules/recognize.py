import os
import cv2
import time
import datetime
import pandas as pd


def mark_security(input_video):
    # reading trained dataset
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("files" + os.sep + "trainer.yml")

    # using haar cascade
    haar_cascade_path = "files" + os.sep + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(haar_cascade_path)

    # preparing pandas dataframe
    df = pd.read_csv("files" + os.sep + "user_details.csv")
    col_names = ['ID', 'Name', 'Date', 'Time']
    security_df = pd.DataFrame(columns=col_names)

    # store input video stream capture in cap variable
    cam = cv2.VideoCapture(input_video)
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        # capture frame-by-frame
        ret, img = cam.read()
        if ret is True:  # video is detected
            # convert frame to grayscale
            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # detect faces using haar cascade detector
            faces = face_cascade.detectMultiScale(gray_frame, 1.2, 5)
            for(x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (225, 0, 0), 2)
                _id, conf = recognizer.predict(gray_frame[y:y+h, x:x+w])

                if conf < 50:
                    current_time = time.time()
                    date = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d')
                    timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
                    user_name = df.loc[df['ID'] == _id]['Name'].values[0]
                    display_text = user_name  # str(_id) + "-" +
                    security_df.loc[len(security_df)] = [_id, user_name, date, timestamp]

                else:
                    display_text = 'Intruder Detected'

                if conf > 75:
                    file_number = len(os.listdir("unknown_images")) + 1
                    cv2.imwrite("unknown_images" + os.sep + "Image" + str(file_number) +
                                ".jpg", img[y:y+h, x:x+w])
                cv2.putText(img, display_text, (x, y+h), font, 1, (255, 255, 255), 2)
            security_df = security_df.drop_duplicates(subset=['ID'], keep='first')
            cv2.imshow('Recognizing Face Survillance - Intrusion Detection System', img)
            if cv2.waitKey(1) == ord('q'):
                break
        else:  # video not detected
            break

    # get current time and date
    current_time = time.time()
    date = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d')
    timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
    hour, minute, second = timestamp.split(":")
  
  
 
    # when everything is done
    cam.release()
    cv2.destroyAllWindows()

    print("Successful!")

   

   
