#!/usr/bin/env python3

""" This program is meant to be an advanced version of the known snapchat filter 
    where there are random images spinning on top of people's heads.
    The main improvement is that you can not only select the images you want to chose from and the caption, 
    as you can play it for more than people SIMULTANEOUSLY.    
"""

from datetime import datetime
import os
import glob
import operator
import sys
import getopt
import cv2
import face_recognition
import numpy as np


def usage():
    '''Print usage in the console'''
    print("\nusage: didifilter.py --location=\"path/to/images/folder\" --caption=\"caption/to/print\"")
    print("                      [--initial=__] [--final=__] [--width=__] [--height=__] [--max=__]")
    print("                      [-v] [--video=__] [--rate=__] [-p] [--picture=__]")
    print("                      [-b, --backward] [-d, --debug] [-h, --help]")

    print("\nThis program is meant to be an advanced version of the known snapchat filter where there are random images spinning on top of people's heads.")
    print("The main improvement is that you can not only select the images you want to chose from and the quote, as you can play it for more than people SIMULTANEOUSLY.")
    print("For that, when giving the location, this must have the following organization:\n")
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
    print("\t--location=\"path/to/images/folder\"     path to the folder that contains the images that are gonna spin randomly")
    print("\t--caption=\"caption/to/print\"           caption that is displayed under randomly spinned image")

    print("\nOptional arguments:")
    print("\t--max=1 (default)                tells the amount of folders with images to the people to expect")
    print("\t--initial=20 (default)           initial time to recognize faces (the time is not seconds but cycles, depends on computer specs)")
    print("\t--final=60 (default)             final time to recognize faces (the time is not seconds but cycles, depends on computer specs)")
    print("\t--width=200 (default)            change width of the images (in pixels) to be resized")
    print("\t--height=200 (default)           change height of the images (in pixels) to be resized")

    print("\t-v                               records a video of the filtering")
    print("\t--video=\"vid\" (default)          selects name of the video of the filtering")
    print("\t--rate=10 (default)              selects speed of video to be recorded")
    print("\t-p                               takes a picture of the final filter")
    print("\t--picturee=\"pic\" (default)       selects name of the video of the filtering")

    print("\t-b, --backward                   allows the images meant for 2,3,.. people to be selected by one person only")
    print("\t-d, --debug                      prints settings used in the game in the console")
    print("\t-h, --help                       show this help message")

    sys.exit(2)


def arg_parse(argv):
    '''Parse arguments provided by the user'''
    try:
        opts, args = getopt.getopt(argv, "hbvpd", ["help", "backward", "location=", "caption=", "debug", "max=", "initial=", "final=", "width=", "height=", "video=", "rate=", "picture="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    s_location = 'memes'
    s_caption = 'WHAT MEME AM I?'
    b_backward = False
    n_max_people = 1
    n_img_width = 200
    n_img_height = 200
    n_initial_time = 20
    n_final_time = 60
    b_video = False
    s_vid_name = "vid"
    n_rate = 7
    b_picture = False
    s_pic_name = "pic"
    b_debug = False

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage()
        elif opt == "--location":
            s_location = arg
        elif opt == "--caption":
            s_caption = arg
        elif opt in ['-d', '--debug']:
            b_debug = True
        elif opt == "--max":
            n_max_people = int(arg)
        elif opt in ['-b', '--backward']:
            b_backward = True
        elif opt == "--initial":
            n_initial_time = int(arg)
        elif opt == "--final":
            n_final_time = int(arg)
        elif opt == "--width":
            n_img_width = int(arg)
        elif opt == "--height":
            n_img_height = int(arg)
        elif opt == '-v':
            b_video = True
        elif opt == "--video":
            s_vid_name = arg
        elif opt == "--rate":
            n_rate = int(arg)
        elif opt == '-p':
            b_picture = True
        elif opt == "--picture":
            s_pic_name = arg


    s_dir_name, s_file_name = os.path.split(os.path.abspath(__file__))

    b_loc_exists = False
    for s_loc_folder in glob.glob(os.path.join(s_dir_name + '/', '*')):
        s_loc_folder_dir, s_loc_folder_name = os.path.split(os.path.abspath(s_loc_folder))
        if s_loc_folder_name == s_location:
            b_loc_exists = True

    if not b_loc_exists:
        print("The location selected is not valid!")
        sys.exit(2)

    if n_max_people > len(glob.glob(os.path.join(s_dir_name + '/' + s_location + '/', '*'))):
        print("The max people selected is not valid!")
        sys.exit(2)

    if b_video or b_picture:
        now = datetime.now()
        s_datetime = now.strftime("%d%m%Y_%H%M%S")

        # If video is selected search if s_vid_name is allowed. If not, add "_DDMMYY_HHMMSS" to it
        if b_video:
            s_video_dir_path = os.path.join(s_dir_name+'/outputs/videos/', '*')
            for videos in glob.glob(s_video_dir_path):
                s_video_dir, s_video_name = os.path.split(os.path.abspath(videos))

                if (s_vid_name + '.avi') == s_video_name:
                    s_vid_name = s_vid_name + '_' + s_datetime

        # If picture is selected search if s_vid_name is allowed. If not, add "_DDMMYY_HHMMSS" to it
        if b_picture:
            s_picture_dir_path = os.path.join(s_dir_name+'/outputs/pictures/', '*')
            for pictures in glob.glob(s_picture_dir_path):
                s_picture_dir, s_picture_name = os.path.split(os.path.abspath(pictures))

                if (s_pic_name + '.png') == s_picture_name:
                    s_pic_name = s_pic_name + '_' + s_datetime

    if b_debug:
        print("The settings used in these game are:")
        print(": location=" + s_location)
        print(": caption=" + s_caption)
        print(": maxPeople=" + str(n_max_people))
        print(": backward compatibility is " + ("disabled", "enabled")[b_backward])
        print(": initial=" + str(n_initial_time) + " cycles")
        print(": final=" + str(n_final_time) + " cycles")
        print(": width=" + str(n_img_width) + " pixels")
        print(": height=" + str(n_img_height) + " pixels")
        if b_video:
            print(": video recording enabled with rate " + str(n_rate) + " and file name " + s_vid_name)
        else:
            print(": video recording disabled")
        if b_picture:
            print(": taking picture at the end enabled with file name " + s_pic_name)
        else:
            print(": taking picture at the end disabled")

    return s_location, s_caption, n_max_people, b_backward, n_initial_time, n_final_time, n_img_width, n_img_height, b_video, s_vid_name, n_rate, b_picture, s_pic_name


if __name__ == "__main__":
    '''Algorithm'''
    # call our own argument parser
    s_location, s_caption, n_max_people, b_backward, n_initial_time, n_final_time, n_img_width, n_img_height, b_video, s_vid_name, n_rate, b_picture, s_pic_name = arg_parse(sys.argv[1:])

    s_dir_name, s_file_name = os.path.split(os.path.abspath(__file__))

    data = []
    a_data_people_edges = [0]

    for i in np.arange(1, n_max_people+1):
        dirPath = os.path.join(s_dir_name+'/'+s_location+'/'+str(i)+'/', '*g')
        s_files_in_dir_path = glob.glob(dirPath)

        a_data_people_edges.append(a_data_people_edges[-1]+int(len(s_files_in_dir_path)))

        for fil in sorted(s_files_in_dir_path):
            img_original = cv2.imread(fil)
            img = cv2.resize(img_original, (n_img_width, n_img_height))
            data.append(img)

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    n_frame_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    n_frame_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Get text size from caption
    n_caption_thickness = 0.7
    n_caption_border = 6
    n_text_width, n_text_height = cv2.getTextSize(s_caption, cv2.FONT_HERSHEY_DUPLEX, n_caption_thickness, 1)[0]

    if (n_img_width > (n_frame_width/2)) or (n_text_width > (n_frame_width/2)) or (n_img_height > (n_frame_height/2)):
        print("Either reduce the size of the image, or select a shorter caption")
        sys.exit(2)

    if b_video:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        vid_out = cv2.VideoWriter(s_dir_name + '/outputs/videos/' + s_vid_name + '.avi', fourcc, n_rate, (int(n_frame_width), int(n_frame_height)))

    face_locations = []
    num_faces = 0
    process_this_frame = True

    t = 0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)

            if len(face_locations) != num_faces:
                t = 0

        num_faces = len(face_locations)

        if num_faces > n_max_people:
            print("There appears to be more people than allowed")
            sys.exit(2)

        process_this_frame = not process_this_frame

        if num_faces > 0:
            t = t+1

            if t > n_initial_time:

                if t < n_initial_time+2:
                    a_random = np.random.permutation(np.arange(a_data_people_edges[num_faces-1], a_data_people_edges[(num_faces, -1)[b_backward]], num_faces))
                    '''
                    if b_backward:
                        a_random = np.random.permutation(np.arange(a_data_people_edges[num_faces-1], a_data_people_edges[-1], num_faces))
                    else:
                        a_random = np.random.permutation(np.arange(a_data_people_edges[num_faces-1], a_data_people_edges[num_faces], num_faces))
                    '''

                j = 0
                # Display the results -  Note the ordering by the face_left, for the memes to appear as requested
                for (face_top, face_right, face_bottom, face_left) in sorted(face_locations, key=operator.itemgetter(3)):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    face_top *= 4
                    face_right *= 4
                    face_bottom *= 4
                    face_left *= 4

                    # Extract image location based on recognized face
                    img_left = int((face_left+face_right-n_img_width)/2)
                    img_right = int((face_left+face_right+n_img_width)/2)
                    img_top = face_top-n_img_height
                    img_bottom = face_top

                    # Extract caption location based on recognized face
                    text_left = int((face_left+face_right-n_text_width)/2)
                    text_right = int((face_left+face_right+n_text_width)/2)
                    text_top = face_top
                    text_bottom = face_top+n_text_height

                    # Check that the image fits within video capture
                    if (face_top >= n_img_height) and (img_left >= 0) and (img_right <= n_frame_width):
                        # Create rectangle for image (from upper-left to bottom-right corner)
                        cv2.rectangle(frame, (img_left, img_top), (img_right, img_bottom), (0, 0, 255), 2)
                        # Create rectangle for caption and print it
                        cv2.rectangle(frame, (text_left-n_caption_border, text_top), (text_right+n_caption_border, text_bottom+2*n_caption_border), (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, s_caption, (text_left, text_bottom+n_caption_border), cv2.FONT_HERSHEY_DUPLEX, n_caption_thickness, (255, 255, 255), 1)

                        if t < n_final_time:
                            frame[img_top:img_bottom, img_left:img_right] = data[a_random[t%len(a_random)]+j]
                        else:
                            frame[img_top:img_bottom, img_left:img_right] = data[a_random[n_final_time%len(a_random)]+j]

                        if b_picture:
                            cv2.imwrite(s_dir_name + '/outputs/pictures/' + s_pic_name + '.png', frame)

                        j = j+1

            if b_video:
                vid_out.write(frame)
        else:
            t = 0

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
