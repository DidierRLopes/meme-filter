#!/usr/bin/env python3

import numpy as np
import cv2
import face_recognition
import os
import glob
import random
import time
import operator
import sys, getopt
from datetime import datetime

def usage():
    print("\nusage: whatMemeAmI.py --locationFolder=\"path/to/images/folder\" --query=\"query/to/print\"")
    print("                      [--initialTime] [--finalTime] [--width] [--height] [--maxPeople]")
    print("                      [-b, --backwardCompatible] [-h, --help]")

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
    print("      The order of the images '_1, _2 and _3' matter. These are assigned from left to right.")

    print("\nThese arguments are a must:")
    print("\t--locationFolder=\"path/to/images/folder\"   path to the folder that contains the images that are gonna spin randomly")
    print("\t--query=\"query/to/print\"                   query that is displayed under randomly spinned image")

    print("\nOptional arguments:")
    print("\t--maxPeople=3 (default)                      tells the amount of folders with images to the people to expect")
    print("\t--initialTime=20 (default)                   initial time to recognize faces (the time is not seconds but cycles, depends on computer specs)")
    print("\t--finalTIme=60 (default)                     final time to recognize faces (the time is not seconds but cycles, depends on computer specs)")
    print("\t--width=200 (default)                        change width of the images (in pixels) to be resized")
    print("\t--height=200 (default)                       change height of the images (in pixels) to be resized")
    print("\t-b, --backwardCompatible                     allows the images meant for 2,3,.. people to be selected by one person only")

    print("\t-v                                           records a video of the filtering")
    print("\t--vName=\"vid\" (default)                    selects name of the video of the filtering")
    print("\t--vRate=10 (default)                         selects speed of video to be recorded")
    print("\t-p                                           takes a picture of the final filter")
    print("\t--pName=\"pic\" (default)                    selects name of the video of the filtering")
    print("\t-h, --help                                   show this help message")
  
    sys.exit(2)

def arg_parse(argv):
    try:
        opts, args = getopt.getopt(argv,"hbvp", ["help", "backwardCompatible", "locationFolder=", "query=", "maxPeople=", "initialTime=", "finalTime=", "width=", "height=", "vName=", "vRate=", "pName="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    
    locationFolder = None
    query = None
    backwardCompatible = False
    maxPeople = 3
    imgWidth = 200
    imgHeight = 200
    initialTime = 20
    finalTime = 60
    video = False
    vName = "vid"
    vRate = 10
    picture = False
    pName = "pic"

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
        elif opt == "--initialTime":
            initialTime = int(arg)
        elif opt == "--finalTime":
            finalTime = int(arg)
        elif opt == "--width":
            imgWidth = int(arg)
        elif opt == "--height":
            imgHeight = int(arg)
        elif opt == '-v':
            video = True
        elif opt == "--vName":
            vName = arg
        elif opt == "--vRate":
            vRate = int(arg)
        elif opt == '-p':
            picture = True
        elif opt == "--pName":
            pName = arg

    if (video or picture):
        dirName, fileName = os.path.split(os.path.abspath(__file__))
        now = datetime.now()
        datetimeString = now.strftime("%d%m%Y_%H%M%S")

        # If video is selected search if vName is allowed. If not, add "_DDMMYY_HHMMSS" to it
        if (video):
            videoDirPath = os.path.join(dirName+'/outputs/videos/','*')
            for videos in glob.glob(videoDirPath):
                videoDirName, videoFileName = os.path.split(os.path.abspath(videos))
        
                if ((vName + '.avi') == videoFileName):
                    vName = vName + '_' + datetimeString

        # If picture is selected search if vName is allowed. If not, add "_DDMMYY_HHMMSS" to it
        if (picture):
            pictureDirPath = os.path.join(dirName+'/outputs/pictures/','*')
            for pictures in glob.glob(pictureDirPath):
                pictureDirName, pictureFileName = os.path.split(os.path.abspath(pictures))

                if ((pName + '.png') == pictureFileName):
                    pName = pName + '_' + datetimeString
    
    # debug arguments - probably we could add verbose levels...
    print("SETTINGS")
    print('locationFolder=' + locationFolder)
    print('query=' + query)
    print('maxPeople=' + str(maxPeople))
    if (backwardCompatible):
        print('backwardCompatible enabled')
    
    print('initialTime=' + str(initialTime) + ' cycles')
    print('finalTime=' + str(finalTime) + ' cycles')
    print('imgWidth=' + str(imgWidth) + ' pixels')
    print('imgHeight=' + str(imgHeight) + ' pixels')
    
    if (video):
        print("recording enabled with rate " + str(vRate) + " and file name " + vName)
    
    if (picture):
        print("taking picture at the end enabled with file name " + pName)

    # check that location and query are not empty, otherwise call usage and exit
    if None in [locationFolder, query]:
        print("Specify both --locationFolder and --query")
        usage()

    return locationFolder, query, maxPeople, backwardCompatible, initialTime, finalTime, imgWidth, imgHeight, video, vName, vRate, picture, pName


if __name__ == "__main__":
    # call our own argument parser
    locationFolder, query, maxPeople, backwardCompatible, initialTime, finalTime, imgWidth, imgHeight, video, vName, vRate, picture, pName = arg_parse(sys.argv[1:])

    dirName, fileName = os.path.split(os.path.abspath(__file__))

    data = []
    dataPeopleEdges = [0]
    dataPeopleImages = []

    for i in np.arange(1, maxPeople+1):
        dirPath = os.path.join(dirName+'/'+locationFolder+str(i)+'/','*g')
        filesInDirPath = glob.glob(dirPath)
        
        dataPeopleEdges.append(dataPeopleEdges[-1]+int(len(filesInDirPath)))
        dataPeopleImages.append(int(len(filesInDirPath)/i))
        
        for fil in sorted(filesInDirPath):
            imgOriginal = cv2.imread(fil)
            img = cv2.resize(imgOriginal, (imgWidth, imgHeight))
            data.append(img)
    
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

    if (video):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        vidOut = cv2.VideoWriter(dirName + '/outputs/videos/' + vName + '.avi', fourcc, vRate, (int(frameWidth),int(frameHeight)))

    faceLocations = []
    numFaces = 0
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
            
            if (len(faceLocations) != numFaces):
                t = 0

        numFaces = len(faceLocations)

        process_this_frame = not process_this_frame

        if (numFaces > 0):
            t = t+1;

            if (t > initialTime):

                if (t < initialTime+2):
                    if (backwardCompatible):
                        print("back numFaces: " + str(numFaces))
                        
                        randomArray = np.random.permutation(np.arange(dataPeopleEdges[numFaces-1], dataPeopleEdges[-1], numFaces))
                        print("back len " + str(len(randomArray)))
                    else:
                        randomArray = np.random.permutation(np.arange(dataPeopleEdges[numFaces-1], dataPeopleEdges[numFaces], numFaces))
                
                j = 0
                # Display the results -  Note the ordering by the faceLeft, for the memes to appear as requested
                for (faceTop, faceRight, faceBottom, faceLeft) in sorted(faceLocations, key=operator.itemgetter(3)):
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
                    
                        print("len random array: " + str(len(randomArray)))
                        print("t: " + str(t))
                        print("j: " + str(j))
                        print("len data: " + str(len(data)))

                        if (t<finalTime):
                            frame[imgTop:imgBottom, imgLeft:imgRight] = data[randomArray[t%len(randomArray)]+j]
                        else:
                            frame[imgTop:imgBottom, imgLeft:imgRight] = data[randomArray[finalTime%len(randomArray)]+j]
                        
                        if (picture):
                            cv2.imwrite(dirName + '/outputs/pictures/' + pName + '.png', frame)

                        j = j+1
            if (video):
                vidOut.write(frame)
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

