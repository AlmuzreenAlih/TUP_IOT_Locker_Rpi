import face_recognition
import cv2
from PIL import Image
import numpy as np
import ctkFunctions as IF

known_image = face_recognition.load_image_file("Cropped1.png")
unknown_image = face_recognition.load_image_file("compare.png")
face_locations = face_recognition.face_locations(unknown_image)
print(face_locations)
# unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)
# ggg = cv2.imread("prev.jpg")
# print(ggg[0][0], unknown_image[0][0])

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
print(results)

import customtkinter as ctk
import cv2

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x480")
font1 = ctk.CTkFont(family='Segoe UI', size=20, weight="bold")

cap = cv2.VideoCapture(0)

def MainLoop():
    _, capt = cap.read()
    unknown_image = face_recognition.load_image_file("Video.png")
    face_locations = face_recognition.face_locations(unknown_image)
    for (top, right, bottom, left) in face_locations:
        # Draw a green rectangle around the face
        cv2.rectangle(capt, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.imwrite("Video.png", capt)
    IF.tkShow(ctk, VideoFeed, "Video.png", 0.5)
    app.after(5, MainLoop)


Form1 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
Form1.place(relx=0.5, rely=0.5, anchor="center")

VideoFeed = ctk.CTkLabel(master=Form1, text="")
VideoFeed.place(relx=0.5, rely=0.5, anchor="center")
IF.tkShow(ctk,VideoFeed, "Video.png",0.5)

def button_function():
    pass

# Login_Button = ctk.CTkButton(master=Form1, font=font1, text="LOGIN", command=button_function, height=50, width=300,
#                              fg_color=("black","yellow"), text_color=("white","black"), corner_radius=10,hover_color="white")
# Login_Button.place(relx=0.5, rely=0.4, anchor="center")


# Register_Button = ctk.CTkButton(master=Form1, font=font1, text="REGISTER", command=button_function, height=50, width=300,
#                                 fg_color=("black","yellow"), text_color=("white","black"), corner_radius=10,hover_color="white")
# Register_Button.place(relx=0.5, rely=0.6, anchor="center")

app.after(5, MainLoop)
app.mainloop()