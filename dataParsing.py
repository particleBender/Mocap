                ###################################
                ##        Anaelisa Aburto        ##
                ##          Data Parsing         ##
                ###################################

# This program allows the user to open a text file containing motion capture data.
# The program creates a new folder if it does not exist and writes the frame data.
# The user may change the frame rate and fix the missing points.
# The program reads the contents of the file, and adds them to a list that is broken
# down into one file for each frame of the animation. The first for loop
# appends the information to a list and splits the elements when the
# program finds a space. The second and third for loop determine the
# distribution of the information in the form of a table or matrix.
# One for loop determines the number of the new frame file, and the other
# determines the row in which the X Y and Z values will be written. 

import sys
from Tkinter import *
from tkFileDialog import askopenfilename
from tkMessageBox import showerror
import os


class mocapApp:

    def __init__(self, master):
        frame = Frame(master)
        # Adapts the size of the window to the size of the text
        frame.pack()

        self.openFile = Button(frame, text="Browse File...", command = self.mocapConverter)
        self.openFile.pack(side=LEFT)

        # Button to quit the app
        self.button = Button(frame, text="Quit", command = frame.quit)
        self.button.pack(side=RIGHT)

        self.radioButton = IntVar()
        self.RB1 = Radiobutton(root, text="24 fps", variable=self.radioButton, value=0)
        self.RB1.pack(side = TOP)
        self.RB1.select()
        self.RB2 = Radiobutton(root, text="30 fps", variable=self.radioButton, value=1)
        self.RB2.pack(side = TOP)
        self.RB3 = Radiobutton(root, text="120 fps", variable=self.radioButton, value=2)
        self.RB3.pack(side = TOP)

        self.checkboxButton = IntVar()
        self.checkbox = Checkbutton(master, text = "Fix Missing Frames", variable = self.checkboxButton)
        self.checkbox.pack(anchor = CENTER)



    # procedure to break down the file into one file per frame
    def mocapConverter(self):
        openFile = askopenfilename(initialdir = '~')

        # tries to open the file, if not possible it displays an error message
        if openFile:
            try:
                sourceFile = open(openFile, "r")
                print("The file loaded successfully")
            except IOError:
                showerror("Open Source File", "Failed to read file\n%s" % openFile)
                sys.exit()

        # tries to create a new folder, if it already exists it ignores the command
        try:
            os.mkdir("Frames")
        except OSError:
            pass

        # reads lines into a list
        text = sourceFile.readlines()
        # closes file
        sourceFile.close()

        # variables
        dataList = []
        frameNumber = 0
        frameRate = 0


        # adds all the lines of the text into a list and separates them into elements
        for line in text:
            dataList.append(line.split())

        # skips first line of the text file since it's information we don't need
        for currentFrame in range(1, len(dataList)):
            # depending on the radio button selection the number of frames dropped changes
            if self.radioButton.get() == 0:
                frameRate = 5
            elif self.radioButton.get() == 1:
                frameRate = 4
            elif self.radioButton.get() == 2:
                frameRate = 1
            
            if currentFrame % frameRate == 0:
                frameNumber = frameNumber + 1

                # this generates frame padding of 4 zeroes
                framePad = 4 - len(str(frameNumber))
                numZero = "0" * framePad
                # generates a new file for the current frame
                newFile = open("Frames\Frame_%s%s.txt" % (numZero, frameNumber), "w")

                line = 0

                for row in range(0, ((len(dataList[currentFrame])-2) /3)):
                    # if the value is -9999.99 it takes the value of the next frame
                     # the values are divided by 100 to make them easily visible in houdini's viewport
                    X = float(dataList[currentFrame][(row*3) + 2])/100
                    if X == -99.9999 and self.checkboxButton.get() == 1:
                        X = ((float(dataList[currentFrame][((row - 1)*3) + 2])/100) + (float(dataList[currentFrame][((row + 1)*3) + 2])/100))/2

                    Y = float(dataList[currentFrame][(row*3) + 3])/100
                    if Y == -99.9999 and self.checkboxButton.get() == 1:
                        Y = ((float(dataList[currentFrame][((row + 1)*3) + 3])/100) + (float(dataList[currentFrame][((row + 1)*3) + 3])/100))/2

                    Z = float(dataList[currentFrame][(row*3) + 4])/100
                    if Z == -99.9999 and self.checkboxButton.get() == 1:
                        Z = ((float(dataList[currentFrame][((row - 1)*3) + 4])/100) + (float(dataList[currentFrame][((row + 1)*3) + 4])/100))/2

                    # writes the x y z information in the new file
                    newFile.write("%s %s %s %s\n" % (line, X, Y, Z))
                    line = line + 1
                # closes the new file
                newFile.close()


# Initialize TKinter
root = Tk()
root.title("Motion Capture File Converter")
# Minimum size for window
root.minsize(300,100)
app = mocapApp(root)

# The program will stay in the event loop until we close the window.
root.mainloop()


