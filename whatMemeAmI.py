#!/usr/bin/env python3

import numpy as np
import cv2
import face_recognition
import os
import glob
import random
import time
import sys, getopt

def usage():
    print("\nusage: whatMemeAmI.py --locationFolder=\"path/to/images/folder\" --query=\"query/to/print\"")
    print("                      [-b, --backwardCompatible] [-h, --help] [--width] [--height] [--maxPeople]")

    print("\nThis program is meant to be an advanced version of the known snapchat filter where there are random images spinning on top of people's heads.")
    print("The main improvement is that you can not only select the images you want to chose from and the quote, as you can play it for more than people SIMULTANEOUSLY.")
    print("For that, when giving the locationFolder, this must have the following organization:\n")
    print("                                          /--- abc.jpg")
    print("path/to/images/folder ------- folder: \"1\" ---- def.jpg")
    print("                         |                \\--- ghi.jpg")
    print("                         |                            ")
    print("                         |                /--- jkl_1.jpg")
    print("                         ---- folder: \"2\" ---- jkl_2.jpg")
    print("                         |                l--- mno_1.jpg")
    print("                         |                \\--- mno_2.jpg")
    print("                         |                            ")
    print("                         |                /--- pqr_1.jpg")
    print("                         |                l--- pqr_2.jpg")
    print("                         ---- folder: \"3\" ---- pqr_3.jpg")
    print("                                          l--- stu_1.jpg")
    print("                                          l--- stu_2.jpg")
    print("                                          \\--- stu_3.jpg")
    print("Note: When there is no folder \"3\" the images used are the ones from the folders above, and so on.")

    print("\nThese arguments are a must:")
    print("\t--locationFolder=\"path/to/images/folder\"     path to the folder that contains the images that are gonna spin randomly")
    print("\t--query=\"query/to/print\"                     query that is displayed under randomly spinned image")

    print("\nOptional arguments:")
    print("\t--maxPeople=3 (default)                      tells the amount of folders with images to the people to expect")
    print("\t--width=200 (default)                        change width of the images (in pixels) to be resized")
    print("\t--height=200 (default)                       change height of the images (in pixels) to be resized")
    print("\t-b, backwardCompatible                       allows the images meant for 2,3,.. people to be selected by one person only")
    print("\t-h, --help                                   show this help message")
  
    sys.exit(2)

def arg_parse(argv):
    try:
        opts, args = getopt.getopt(argv,"hb", ["help", "backwardCompatible", "locationFolder=", "query=", "maxPeople=", "width=", "height="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    
    locationFolder = None
    query = None
    backwardCompatible = False
    maxPeople = 3
    imgWidth = 200
    imgHeight = 200

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage();
        elif opt == "--locationFolder":
            locationFolder = arg
        elif opt == "--query":
            query = arg
        elif opt == "--maxPeople":
            maxPeople = int(arg)
        elif opt in ['-b', '--backwardCompatible']:
            backwardCompatible = True
        elif opt == "--width":
            imgWidth = int(arg)
        elif opt == "--height":
            imgHeight = int(arg)
    
    # debug arguments - probably we could add verbose levels...
    print([locationFolder, query, maxPeople, backwardCompatible, imgWidth, imgHeight])

    # check that location and query are not empty, otherwise call usage and exit
    if None in [locationFolder, query]:
        print("Specify both --locationFolder and --query")
        usage()

    return locationFolder, query, maxPeople, backwardCompatible, imgWidth, imgHeight

if __name__ == "__main__":
    # call our own argument parser
    locationFolder, query, maxPeople, backwardCompatible, imgWidth, imgHeight = arg_parse(sys.argv[1:])

    dirname, filename = os.path.split(os.path.abspath(__file__))
    
    data = []
    dataPeopleEdges = [0]
    dataPeopleImages = []

    for i in np.arange(1, maxPeople+1):
        dir_path = os.path.join(dirname+'/'+locationFolder+str(i)+'/','*g')
        files_in_dir_path = glob.glob(dir_path)
        
        dataPeopleEdges.append(dataPeopleEdges[-1]+int(len(files_in_dir_path)))
        dataPeopleImages.append(int(len(files_in_dir_path)/i))
        
        for fil in sorted(files_in_dir_path):
            img_original = cv2.imread(fil)
            img = cv2.resize(img_original, (imgWidth, imgHeight))
            data.append(img)

    # something like data[MAXPEOPLE1:MAXPEOPLE2] = [(1,2),(3,4),(5,6),(7,8)]
    # but then how to access the corresponding images? by tuples?

    # Check that there is actually images, otherwise use a sad image perhaps?

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    frameWidth = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH )
    frameHeight = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT )
   
    # Get text size from query
    queryThickness = 0.7
    queryBorder = 6
    textWidth, textHeight = cv2.getTextSize(query, cv2.FONT_HERSHEY_DUPLEX, queryThickness, 1)[0]
    
    if (imgWidth > (frameWidth/2) or textWidth > (frameWidth/2) or imgHeight > (frameHeight/2)):
        print("Either reduce the size of the image, or select a shorter query")
        sys.exit(2)
    
    faceLocations = []
    process_this_frame = True

    t = 0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()


        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgbSmallFrame = smallFrame[:, :, ::-1]
            # Find all the faces and face encodings in the current frame of video
            faceLocations = face_recognition.face_locations(rgbSmallFrame)
     
        process_this_frame = not process_this_frame

        if (len(faceLocations) > 0):
            t = t+1;

            if (t > 20):
                # Display the results
                for (faceTop, faceRight, faceBottom, faceLeft) in faceLocations:
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    faceTop *= 4
                    faceRight *= 4
                    faceBottom *= 4
                    faceLeft *= 4
                   
                    # Extract image location based on recognized face
                    imgLeft = int((faceLeft+faceRight-imgWidth)/2)
                    imgRight = int((faceLeft+faceRight+imgWidth)/2)
                    imgTop = faceTop-imgHeight
                    imgBottom = faceTop

                    # Extract query location based on recognized face
                    textLeft = int((faceLeft+faceRight-textWidth)/2)
                    textRight = int((faceLeft+faceRight+textWidth)/2)
                    textTop = faceTop
                    textBottom = faceTop+textHeight

                    # Check that the image fits within video capture
                    if (faceTop >= imgHeight and imgLeft >= 0 and imgRight <= frameWidth ):
                        # Create rectangle for image (from upper-left to bottom-right corner)
                        cv2.rectangle(frame, (imgLeft, imgTop), (imgRight, imgBottom), (0, 0, 255), 2)
                        # Create rectangle for query and print it
                        cv2.rectangle(frame, (textLeft-queryBorder, textTop), (textRight+queryBorder, textBottom+2*queryBorder), (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, query, (textLeft, textBottom+queryBorder), cv2.FONT_HERSHEY_DUPLEX, queryThickness, (255, 255, 255), 1)
                    
                        if (t < 60):
                            # iterate randomly through meme dataset
                            randomArray = np.random.permutation(len(data))
                            for i in randomArray:
                                frame[imgTop:imgBottom, imgLeft:imgRight] = data[i]
                        elif (t < 50):
                            frame[imgTop:imgBottom, imgLeft:imgRight] = data[randomArray[0]]
                        elif (t < 52):
                            frame[imgTop:imgBottom, imgLeft:imgRight] = data[randomArray[1]]
                        elif (t < 55):
                            frame[imgTop:imgBottom, imgLeft:imgRight] = data[randomArray[2]]
                        else:
                            frame[imgTop:imgBottom, imgLeft:imgRight] = data[randomArray[0]]
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
