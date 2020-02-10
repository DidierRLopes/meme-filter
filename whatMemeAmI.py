#!/usr/bin/env python3

import numpy as np
import cv2
import face_recognition
import os
import glob
import random
import time

dirname, filename = os.path.split(os.path.abspath(__file__))

dir_path = os.path.join(dirname+'/memes_1','*g')

data = []
for fil in glob.glob(dir_path):
    img_original = cv2.imread(fil)
    img = cv2.resize(img_original, (200, 200))
    data.append(img)


#print(data)

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

width_frame = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH )
height_frame = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT )

# Initialize some variables
face_locations = []
process_this_frame = True

#di_img = cv2.imread("memes_1/didi.jpeg")
#di_img = cv2.resize(data[2], (200, 200))

t = 0
j = 0
while True:
    print(t)

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
 
    process_this_frame = not process_this_frame

    if (len(face_locations) > 0):
        t = t+1;

        if (t > 20):    
            # Display the results
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                name = "WHAT MEME AM I?"

                # Draw a box around the face
                #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                centerMiddle = left + int((right-left)/2) - 100
                
                # the meme image fits in the video capture
                if (top >= 200 and centerMiddle >= 0 and (centerMiddle+200) <= width_frame ):
                    # adjust rectangle accordingly
                    cv2.rectangle(frame, (centerMiddle, top-200), (centerMiddle+200, top), (0, 0, 255), 2)
                    cv2.rectangle(frame, (centerMiddle, top), (centerMiddle+200,
                        top+20), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (centerMiddle + 8, top + 16), font, 0.6, (255, 255, 255), 1)
                
                    if (t < 60):
                        # iterate randomly through meme dataset
                        randomArray = np.random.permutation(len(data))
                        for i in randomArray:
                            frame[top-200:top, centerMiddle:centerMiddle+200] = data[i]
                    elif (t < 50):
                        frame[top-200:top, centerMiddle:centerMiddle+200] = data[randomArray[0]]
                    elif (t < 52):
                        frame[top-200:top, centerMiddle:centerMiddle+200] = data[randomArray[1]]
                    elif (t < 55):
                        frame[top-200:top, centerMiddle:centerMiddle+200] = data[randomArray[2]]
                    else:
                        frame[top-200:top, centerMiddle:centerMiddle+200] = data[randomArray[0]]
    else:
        t = 0;

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
