import time
import customtkinter as ctk
import cv2
from ctkFunctions import *
import face_recognition
from tkinter import messagebox
from databaseFunctions import *
import serial
# SerialData = serial.Serial("/dev/ttyUSB0", 9600, timeout = 0.2)
###SerialData = serial.Serial("com10", 9600, timeout = 0.2)
# SerialData.setDTR(False)
# time.sleep(1)
# SerialData.flushInput()
# SerialData.setDTR(True)
time.sleep(2)

DB_Insert = DB_InsertC()
DB_Updater = DB_UpdaterC()

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x480")
font0 = ctk.CTkFont(family='Segoe UI', size=40, weight="bold",slant="italic")
font1 = ctk.CTkFont(family='Segoe UI', size=20, weight="bold")
font2 = ctk.CTkFont(family='Segoe UI', size=14)

cap = cv2.VideoCapture(0)

GUI1 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
GUI1.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI1, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkShow(ctk,bg,"logo2.png",1)

def button_function():
    pass

Login_Button = ctk.CTkButton(master=GUI1, font=font0, text="TIME IN", command=button_function, height=80, width=500,
                             fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
Login_Button.place(relx=0.06, rely=0.16, anchor="nw")

Logout_Button = ctk.CTkButton(master=GUI1, font=font0, text="TIME OUT", command=button_function, height=80, width=500,
                             fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
Logout_Button.place(relx=0.5, rely=0.5, anchor="center")

def Register_Button_Function():
    global Process
    tkPack(GUI2)
    tkHide(GUI1)
    Process = 1
    
Register_Button = ctk.CTkButton(master=GUI1, font=font0, text="REGISTER", command=Register_Button_Function, height=80, width=500,
                                fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
Register_Button.place(relx=0.32, rely=0.67, anchor="nw")

##########################################################################################################################
CropWidth = 250
CropHeight = 250
Steady = 0
Captured = 0
Process = 0
def MainLoop():
    global Process
    # print(Process)
    if Process == 1:
        _, capt = cap.read()
        global Steady
        global Captured
        Captured, ToReturn = 0, 0
        cv2.imwrite("Orig.png", capt)
        height, width, _ = capt.shape
        left, top = int((width - CropWidth) / 2), int((height - CropHeight) / 2)
        right, bottom = left + CropWidth, top + CropHeight
        
        unknown_image = face_recognition.load_image_file("Orig.png")
        face_locations = face_recognition.face_locations(unknown_image)
        color = (0, 0, 255)
        delay = 8
        if len(face_locations) > 0: 
            top2, right2, bottom2, left2 = face_locations[0]
            face_center = [(left2 + right2) // 2, (top2 + bottom2) // 2]
            adjX, adj = 90, 75
            if face_center[0] - adjX > left and face_center[0] + adjX < right and face_center[1] - adj > top  and face_center[1] + adj < bottom: 
                color = (0, 255, 0)
                Steady = Steady + 1
                Status_label.configure(text="Center your face within the box.\nSteady. "+str(int(Steady/delay)))
                if int(Steady/delay) > 2:
                    ToReturn = 1
            else:
                Steady = 0 
                Status_label.configure(text="Center your face within the box.")
                
            cv2.circle(capt, (face_center[0], face_center[1]), 5, color, -1)
        else:
            Steady = 0 
            Status_label.configure(text="Center your face within the box.")
            
        cv2.rectangle(capt, (left, top), (right, bottom), color, 2)
        cropped = cv2.imread("Orig.png")[top:bottom, left:right]
        cv2.imwrite("Cropped.png", cropped)
        
        if ToReturn == 0:
            cv2.imwrite("Video.png", capt)
            tkShow(ctk,VideoFeed,"Video.png",0.45)

        else:
            Steady, Captured = 0, 1
            cv2.imwrite("Video.png", cropped)
            tkShow(ctk,VideoFeed,"Video.png",0.9)
            Status_label.configure(text='Press "R" to retake picture.')
            Process = 0
    app.after(5,MainLoop)
    
GUI2 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
# GUI2.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI2, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkShow(ctk,bg,"bg2.png",1)

X1 = 0.05
Y1 = 0.05
Yd = 0.1
width1 = 420
height1 = 37
label = ctk.CTkLabel(master=GUI2, font=font1, text="REGISTRATION FORM", fg_color="white")
label.place(relx=X1, rely=Y1+0*Yd, anchor="nw")

Name1Entry = ctk.CTkEntry(master=GUI2, placeholder_text="Enter First Name", width=width1,height=height1, border_width=2, 
                     corner_radius=8, font=font2)
Name1Entry.place(relx=X1, rely=Y1+1*Yd, anchor="nw")

Name2Entry = ctk.CTkEntry(master=GUI2, placeholder_text="Enter Middle Name", width=width1,height=height1, border_width=2, 
                     corner_radius=8, font=font2)
Name2Entry.place(relx=X1, rely=Y1+2*Yd, anchor="nw")

Name3Entry = ctk.CTkEntry(master=GUI2, placeholder_text="Enter Last Name", width=width1,height=height1, border_width=2, 
                     corner_radius=8, font=font2)
Name3Entry.place(relx=X1, rely=Y1+3*Yd, anchor="nw")

ContactEntry = ctk.CTkEntry(master=GUI2, placeholder_text="Enter Contact Number", width=width1,height=height1, border_width=2, 
                     corner_radius=8, font=font2)
ContactEntry.place(relx=X1, rely=Y1+4*Yd, anchor="nw")

Status_label = ctk.CTkLabel(master=GUI2, font=font1, text="Image ID", fg_color="white")
Status_label.place(relx=0.79, rely=Y1+0*Yd, anchor="n")

VideoFeed = ctk.CTkLabel(master=GUI2, text="")
VideoFeed.place(relx=0.8, rely=0.35, anchor="center")
# tkShow(ctk,VideoFeed, "Video.png",0.5)

Status_label = ctk.CTkLabel(master=GUI2, font=font1, text="Center your face within the box.", fg_color="white")
Status_label.place(relx=0.8, rely=0.60, anchor="n")
    
def Error1():
    FingerPrintStatus.configure(text="Put your finger on the reader.")

All = DB_SelectAll(db=db, table="users")

def GetLeastAvailable():
    global All
    list1 = []
    for a in All:
        list1.append(a[1])

    return min(list1) - 1

def Success1():
    global db
    Name1 = Name1Entry.get()
    Name2 = Name2Entry.get()
    Name3 = Name3Entry.get()
    CNs = ContactEntry.get()
    
    DB_Insert.Init(db=db, table="users")
    DB_Insert.Add(["first_name",Name1])
    DB_Insert.Add(["middle_name",Name2])
    DB_Insert.Add(["last_name",Name3])
    DB_Insert.Add(["contact_number",CNs])
    DB_Insert.Add(["finger_id",str(GetLeastAvailable())])
    DB_Insert.Add(["start_time",str(time.time())])
    DB_Insert.Commit()    
    copy("Cropped.png", "Images", str(DB_SelectAll(db=db,table="users")[-1][0]) + ".png")
    
    tkHide(FingerPrintPanel)
    tkPack(GUI1)
    tkHide(GUI2)
    FingerPrintStatus.configure(text="Put your finger on the reader.")
    Name1Entry.delete(0,-1)
    Name2Entry.delete(0,-1)
    Name3Entry.delete(0,-1)
    ContactEntry.delete(0,-1)
    
def Proceed_Button1_Func():
    global Captured
    Name1 = Name1Entry.get()
    Name2 = Name2Entry.get()
    Name3 = Name3Entry.get()
    CNs = ContactEntry.get()
    if Name1 == "" or Name2 == "" or Name3 == "" or CNs=="":
        messagebox.showerror('Error', 'Please fill all fields')
        return
    elif Captured == 0:
        messagebox.showerror('Error', 'Please finish the camera capturing instruction.')
        return
    else:
        ask = messagebox.askquestion('Confirmation', 'Are you sure?')
        if ask == "yes":    
            ###SerialData.write(bytes(str(GetLeastAvailable()), "utf-8"))
            FingerPrintPanel.place(relx=0.5, rely=0.5, anchor="center")
        
    app.after(5, Loop2)

Proceed_Button1 = ctk.CTkButton(master=GUI2, font=font1, text="SUBMIT", command=Proceed_Button1_Func, height=37, width=150,
                             fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Proceed_Button1.place(relx=0.575, rely=0.56, anchor="ne")

Back_Button1 = ctk.CTkButton(master=GUI2, font=font1, text="BACK", command=button_function, height=37, width=150,
                             fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Back_Button1.place(relx=0.05, rely=0.56, anchor="nw")

FingerPrintPanel = ctk.CTkFrame(master=GUI2, width=600, height=290, fg_color="gray85", corner_radius=9, border_width=2)
# FingerPrintPanel.place(relx=0.5, rely=0.5, anchor="center")

FingerPrintImg = ctk.CTkLabel(master=FingerPrintPanel, text="", width=100, height=100, fg_color="gray40", corner_radius=9)
FingerPrintImg.place(relx=0.1, rely=0.5, anchor="w")
tkShow(ctk, FingerPrintImg, "f1.png", 0.25)

FingerPrintStatus = ctk.CTkLabel(master=FingerPrintPanel, font=font1, text="Please put your finger on the reader.", corner_radius=9)
FingerPrintStatus.place(relx=0.35, rely=0.5, anchor="w")

def key_input(event):
    if event.char == "r":
        app.after(5, MainLoop)
    
app.after(5,MainLoop)
app.bind("<KeyPress>", key_input)
app.mainloop()