import cv2 as cv2
import imutils
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import numpy as np
import serial
import time
import datetime
import ImportantFunctions as IF


root=tk.Tk()    #Main Root
root.attributes('-fullscreen', True)
##root.state('normal')
root.configure(background='white')
subFont1 = tkinter.font.Font(family='Segoe UI', size = 20, weight = "bold")
subFont2 = tkinter.font.Font(family='Segoe UI', size = 15, weight = "bold")
subFont3 = tkinter.font.Font(family='Segoe UI', size = 12, weight = "bold")

cap = cv2.VideoCapture(0)

def MainLoop():
    _, capt = cap.read()
    cv2.imwrite("Video.png", capt)
    IF.tkShow2(VideoFeed,"Video.png",0.25)
    root.after(5,MainLoop)
    

GUI1 = tk.Frame(root)
GUI1.pack()

IF.Create_White_Screen("bg1.png", root.winfo_screenwidth(), root.winfo_screenheight())
Background = tk.Label(GUI1, text='',font = subFont1, bg='white',bd=0)
Background.pack()
IF.tkShow2(Background, "bg1.png", 1)

VideoFeed = tk.Label(GUI1, text='', font = subFont1, bg='white')
VideoFeed.place(x=30,y=50)

root.after(5,MainLoop)
root.mainloop()
