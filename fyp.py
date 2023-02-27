#Importing_libraries
from __future__ import print_function
import tkinter as tk
from typing import Type, Union
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import imutils
import cv2
import os
import time
import argparse
from PIL.ImageTk import PhotoImage
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import time
import dlib
import pyautogui
import serial


ser = serial.Serial('/dev/ttyACM0', 9600)


large_font = ("verdana", 12)


#calculating EAR
def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
#function that makes the sound 'YES'
def yes():
    os.system("mpg123 " + "yes.mp3")
#function that makes the sound 'NO'
def no():
    os.system("mpg123 " + "NO.mp3")
#BLUETOOTH------------------------------------
def switch1():
    ser.write('a'.encode())
def switch2():
    ser.write('b'.encode())
def switch3():
    ser.write('c'.encode())
def switch4():
    ser.write('d'.encode())
#GSM------------------------------------------
def sms1():
    ser.write('p'.encode())
def sms2():
    ser.write('q'.encode())
def sms3():
    ser.write('r'.encode())
def sms4():
    ser.write('s'.encode())
def sms5():
    ser.write('t'.encode())
def sms6():
    ser.write('u'.encode())
def sms7():
    ser.write('v'.encode())
def sms8():
    ser.write('x'.encode())


#Main class of the program
class windows(tk.Tk):


    def __init__(self,vs,*args, **kwargs):
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None


        self.root = tk.Tk()

        self.panel = None
        #background window
        self.root.geometry("420x500+250+127")
        self.root.configure(borderwidth="2", bg="#d5e4e5")
        self.root.wm_title("FYP")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


        # start a thread that constantly pools the video sensor for the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        tk.Frame.__init__(self,*args, **kwargs)
        container = tk.Frame(self.root)
        container.configure(relief='groove')
        #container.configure(borderwidth="2")
        container.configure(relief='groove')
        container.configure(width=250)
        self.framez = None
        #button's container height
        container.place(relx=0.09, rely=0.089, relheight=0.866, relwidth=0.80)
        ##################All_frames###################
        self.frames = {}
        # add pages here
        for f in (startpage, MESSAGES, TEMPLATES, TEMPLATES2, Controlling_Appliances):
            self.framez = f(container, self)
            self.frames[f] = self.framez

        self.show_frame(startpage)

    def show_frame(self, cont):

        newframe = self.frames[cont]
        if self.framez is not None:
            self.framez.place_forget()
        self.framez = newframe
        self.framez.place(relx=0, rely=0, relheight=1, relwidth=1)


    ############//////#All_frames////////############



    def videoLoop(self):
        # 00000000000000000000---BLINKS----00000000000000000#

        # define two constants, one for the eye aspect ratio to indicate
        # blink and then a second constant for the number of consecutive
        # frames the eye must be below the threshold

        EYE_AR_THRESH = 0.272 	
        EYE_AR_CONSEC_FRAMES = 16	
        Enter=48
        sleep=100
	

        # initialize the frame counters and the total number of blinks
        COUNTER = 0
        TOTAL = 0
        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print(	"[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        # grab the indexes of the facial landmarks for the left and right eye, respectively
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        # 00000000000000000000---BLINKS----00000000000000000#


        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 370 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame,width=370)
                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                #00000000000000000000---BLINKS----00000000000000000#
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                rects = detector(gray, 0)
                # loop over the face detections
                for rect in rects:
                    # determine the facial landmarks for the face region, then
                    # convert the facial landmark (x, y)-coordinates to a NumPy
                    # array
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)

                    # extract the left and right eye coordinates, then use the
                    # coordinates to compute the eye aspect ratio for both eyes
                    leftEye = shape[lStart:lEnd]
                    rightEye = shape[rStart:rEnd]
                    leftEAR = eye_aspect_ratio(leftEye)
                    rightEAR = eye_aspect_ratio(rightEye)
                    # average the eye aspect ratio together for both eyes
                    ear = (leftEAR + rightEAR) / 2.0

                    # compute the convex hull for the left and right eye, then
                    # visualize each of the eyes
                    leftEyeHull = cv2.convexHull(leftEye)
                    rightEyeHull = cv2.convexHull(rightEye)
                    cv2.drawContours(self.frame, [leftEyeHull], -1, (0, 255, 0), 1)
                    cv2.drawContours(self.frame, [rightEyeHull], -1, (0, 255, 0), 1)
                    # check to see if the eye aspect ratio is below the blink
                    # threshold, and if so, increment the blink frame counter
                    if ear < EYE_AR_THRESH:
                        COUNTER += 1

                    # otherwise, the eye aspect ratio is not below the blink
                    # threshold
                    else:
                        # if the eyes were closed for a sufficient number of
                        # then increment the total number of blinks
                        if COUNTER >= EYE_AR_CONSEC_FRAMES and COUNTER<=Enter:
                            TOTAL += 1
                            pyautogui.press('tab')
                        elif  COUNTER>=Enter and COUNTER<=sleep:
                            pyautogui.press('space')

                        COUNTER = 0
                        ####################
                        # count = tk.IntVar()
                        #counter = tk.Label(self.root, text="Blinks")
                        #counter.place(x=10, y=290)
                        #numberofcounts = tk.Label(self.root, textvariable=count)
                        #numberofcounts.place(x=60, y=290)
                        #count.set(TOTAL)
                        #################
                        # reset the eye frame counter
                        # draw the total number of blinks on the frame along with
                        # the computed eye aspect ratio for the frame
                        #cv2.putText(self.frame, "Blinks: {}".format(TOTAL), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0, 0, 255), 2)
                        #cv2.putText(self.frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0, 0, 255), 2)
                # show the frame
                cv2.imshow("Frame",self.frame)
                cv2.moveWindow("Frame", 672, 127)
                key = cv2.waitKey(1) & 0xFF
                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
            # 00000000000000000000---BLINKS----00000000000000000#

                # if the panel is not None, we need to initialize it
                #if self.panel is None:
                #    self.panel = tk.Label(image=image)
                #    self.panel.image = image
                #    self.panel.configure(relief='groove')
                #    self.panel.configure(borderwidth="0")
                #    self.panel.configure(width=370,height=350,bg="#d5e4e5")
                #    self.panel.place(relx=0.50, rely=0.089, relheight=0.62, relwidth=0.40)

                # otherwise, simply update the panel
                #else:
                #    self.panel.configure(image=image)
                #    self.panel.image = image


        except RuntimeError:

            print('[INFO] caught a RuntimeError')

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of the quit process to continue

        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

####################ALL_pages#####################
class startpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg="lightsteelblue", width=235,height=350)

        label = tk.Label(self, text="HOME ", font=large_font,fg = 'white')
        label.configure(background="#383dd8")
        label.place(relx=0.0, rely=0.0, relheight=0.093, relwidth=0.999)

        button1 = tk.Button(self, text="SAY YES",command=yes,activebackground = '#33B5e5', bg = 'steelblue', fg = 'white')
        button1.place(relx=0.355, rely=0.202, height=30, width=97)

        button2 = tk.Button(self, text="SAY NO",command=no,activebackground = '#33B5e5', bg = 'steelblue', fg = 'white')
        button2.place(relx=0.355, rely=0.347, height=30, width=97)


        button3 = tk.Button(self, text="MESSAGES",activebackground = '#33B5e5', bg = 'steelblue', fg = 'white', command=lambda: controller.show_frame(MESSAGES))
        button3.place(relx=0.355, rely=0.52, height=30, width=97)

        button4 = tk.Button(self, text="CONTROLLING APPLIANCES",activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=lambda: controller.show_frame(Controlling_Appliances))
        button4.place(relx=0.21, rely=0.694, height=30, width=197)

        button5 = tk.Button(self, text="ENTERTAINMENT", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=lambda: controller.show_frame(MESSAGES))
        button5.place(relx=0.330, rely=0.838, height=24, width=120)



class MESSAGES(tk.Frame):
    def __init__(self,parent,controller):
       tk.Frame.__init__(self,parent)
       tk.Frame.configure(self, bg="lightsteelblue", width=235,height=350)

       label=tk.Label(self, text="MESSAGES", font=large_font)
       label.configure(background="#383dd8")
       label.place(relx=0.0, rely=0.0, relheight=0.093, relwidth=0.999)

       button1=tk.Button(self,text="SAY YES",command=yes,activebackground = '#33B5e5', bg = 'steelblue', fg = 'white')
       button1.place(relx=0.355, rely=0.202, height=24, width=97)

       button2 = tk.Button(self, text="SAY NO",command=no,activebackground = '#33B5e5', bg = 'steelblue', fg = 'white')
       button2.place(relx=0.355, rely=0.347, height=24, width=97)

       button3 = tk.Button(self, text="Templates1",activebackground = '#33B5e5', bg = 'steelblue', fg = 'white' ,command=lambda: controller.show_frame(TEMPLATES))
       button3.place(relx=0.355, rely=0.52, height=24, width=97)

       button4 = tk.Button(self, text="Templates2", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=lambda: controller.show_frame(TEMPLATES2))
       button4.place(relx=0.355, rely=0.694, height=24, width=97)

       button5 = tk.Button(self, text="Back", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=lambda: controller.show_frame(startpage))
       button5.place(relx=0.355, rely=0.838, height=24, width=87)
####################################################
class TEMPLATES(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg="lightsteelblue", width=235, height=350)

        label = tk.Label(self, text="TEMPLATES", font=large_font)
        label.configure(background="#383dd8")
        label.place(relx=0.0, rely=0.0, relheight=0.093, relwidth=0.999)

        button1 = tk.Button(self, text="I NEED BATH", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=sms1)
        button1.place(relx=0.355, rely=0.26, height=24, width=97)

        button2 = tk.Button(self, text="I NEED HELP", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=sms2)
        button2.place(relx=0.355, rely=0.376, height=24, width=97)

        button3 = tk.Button(self, text="I NEED WATER", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=sms3)
        button3.place(relx=0.355, rely=0.491, height=24, width=97)

        button4 = tk.Button(self, text="I NEED FOOD", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=sms4)
        button4.place(relx=0.355, rely=0.607, height=24, width=97)

        button5 = tk.Button(self, text="More..", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=lambda: controller.show_frame(TEMPLATES2))
        button5.place(relx=0.39, rely=0.723, height=24, width=67)

        button6 = tk.Button(self, text="Back..", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=lambda: controller.show_frame(startpage))
        button6.place(relx=0.39, rely=0.838, height=24, width=71)

        ################################
class TEMPLATES2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg="lightsteelblue", width=235,height=350)

        label = tk.Label(self, text="TEMPLATES2", font=large_font)
        label.configure(background="#383dd8")
        label.place(relx=0.0, rely=0.0, relheight=0.093, relwidth=0.999)

        button1 = tk.Button(self, text="I NEED BATH", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=sms5)
        button1.place(relx=0.355, rely=0.231, height=24, width=97)

        button2 = tk.Button(self, text="I NEED HELP", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=sms6)
        button2.place(relx=0.355, rely=0.376, height=24, width=97)

        button3 = tk.Button(self, text="I NEED WATER", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=sms7)
        button3.place(relx=0.355, rely=0.52, height=24, width=97)

        button4 = tk.Button(self, text="I NEED FOOD", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=sms8)
        button4.place(relx=0.355, rely=0.665, height=24, width=97)

        button5 = tk.Button(self, text="Back", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=lambda: controller.show_frame(MESSAGES))
        button5.place(relx=0.39, rely=0.809, height=24, width=71)
        ##################################

class Controlling_Appliances(tk.Frame):
     def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            tk.Frame.configure(self, bg="lightsteelblue", width=235,height=350)

            label = tk.Label(self, text="Contolling Appliances", font=large_font)
            label.configure(background="#383dd8")
            label.place(relx=0.0, rely=0.0, relheight=0.093, relwidth=0.999)

            button1 = tk.Button(self, text="Switch 1", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=switch1)
            button1.place(relx=0.355, rely=0.231, height=24, width=97)

            button2 = tk.Button(self, text="Switch2", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=switch2)
            button2.place(relx=0.355, rely=0.376, height=24, width=97)

            button3 = tk.Button(self, text="Switch3", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=switch3)
            button3.place(relx=0.355, rely=0.52, height=24, width=97)

            button4 = tk.Button(self, text="Switch4", activebackground = '#33B5e5', bg = 'steelblue', fg = 'white',command=switch4)
            button4.place(relx=0.355, rely=0.665, height=24, width=97)

            button5 = tk.Button(self, text="HOME",activebackground = '#33B5e5', bg = 'steelblue', fg = 'white' ,command=lambda: controller.show_frame(startpage))
            button5.place(relx=0.39, rely=0.809, height=24, width=71)
       ######################

vs = VideoStream(1).start()
time.sleep(2.0)

app = windows(vs)
app.mainloop()








