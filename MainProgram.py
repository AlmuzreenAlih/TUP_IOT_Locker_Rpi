import customtkinter as ctk
import cv2
from ctkFunctions import *
import face_recognition

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x480")
font1 = ctk.CTkFont(family='Segoe UI', size=20, weight="bold")
font2 = ctk.CTkFont(family='Segoe UI', size=14)

cap = cv2.VideoCapture(0)

GUI1 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
# GUI1.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI1, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkShow(ctk,bg,"bg2.png",1)

def button_function():
    pass

Login_Button = ctk.CTkButton(master=GUI1, font=font1, text="TIME IN", command=button_function, height=50, width=300,
                             fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Login_Button.place(relx=0.5, rely=0.35, anchor="center")

Logout_Button = ctk.CTkButton(master=GUI1, font=font1, text="TIME OUT", command=button_function, height=50, width=300,
                             fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Logout_Button.place(relx=0.5, rely=0.5, anchor="center")

def Register_Button_Function():
    tkPack(GUI2)
    tkHide(GUI1)
    
Register_Button = ctk.CTkButton(master=GUI1, font=font1, text="REGISTER", command=Register_Button_Function, height=50, width=300,
                                fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Register_Button.place(relx=0.5, rely=0.65, anchor="center")

##########################################################################################################################
CropWidth = 250
CropHeight = 250
Steady = 0
def MainLoop():
    _, capt = cap.read()
    global Steady
    ToReturn = 0
    cv2.imwrite("Orig.png", capt)
    
    # Get the dimensions of the image
    height, width, _ = capt.shape
    left = int((width - CropWidth) / 2)
    top = int((height - CropHeight) / 2)
    right = left + CropWidth
    bottom = top + CropHeight
    
    unknown_image = face_recognition.load_image_file("Orig.png")
    face_locations = face_recognition.face_locations(unknown_image)
    color = (0, 0, 255)
    delay = 8
    if len(face_locations) > 0: 
        top2, right2, bottom2, left2 = face_locations[0]
        face_center = [(left2 + right2) // 2, (top2 + bottom2) // 2]
        adjX = 90
        adj = 75
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
        app.after(5,MainLoop)
    else:
        Steady = 0
        cv2.imwrite("Video.png", cropped)
        tkShow(ctk,VideoFeed,"Video.png",0.9)
        Status_label.configure(text='Press "R" to retake picture.')
        return

GUI2 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
GUI2.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI2, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkShow(ctk,bg,"bg2.png",1)

X1 = 0.05
Y1 = 0.05
Yd = 0.1
width1 = 400
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

Status_label = ctk.CTkLabel(master=GUI2, font=font1, text="Biometrics: ", fg_color="white")
Status_label.place(relx=0.6, rely=Y1+0*Yd, anchor="nw")

VideoFeed = ctk.CTkLabel(master=GUI2, text="")
VideoFeed.place(relx=0.8, rely=0.35, anchor="center")
# tkShow(ctk,VideoFeed, "Video.png",0.5)

Status_label = ctk.CTkLabel(master=GUI2, font=font1, text="Center your face within the box.", fg_color="white")
Status_label.place(relx=0.8, rely=0.60, anchor="n")

Back_Button1 = ctk.CTkButton(master=GUI2, font=font1, text="BACK", command=button_function, height=50, width=300,
                             fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Back_Button1.place(relx=0.35, rely=0.8, anchor="center")

Proceed_Button1 = ctk.CTkButton(master=GUI2, font=font1, text="SUBMIT", command=button_function, height=50, width=300,
                             fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Proceed_Button1.place(relx=0.35, rely=0.8, anchor="center")

def key_input(event):
    if event.char == "r":
        app.after(5, MainLoop)
    
app.bind("<KeyPress>", key_input)
app.mainloop()