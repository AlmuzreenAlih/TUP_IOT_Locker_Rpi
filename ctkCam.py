import customtkinter as ctk
import cv2
from ctkFunctions import *

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x480")
font1 = ctk.CTkFont(family='Segoe UI', size=20, weight="bold")

cap = cv2.VideoCapture(0)

def MainLoop():
    _, capt = cap.read()
    cv2.imwrite("Video.png", capt)
    tkRender(ctk,VideoFeed,"Video.png",0.5)
    app.after(5,MainLoop)

Form1 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
Form1.place(relx=0.5, rely=0.5, anchor="center")

VideoFeed = ctk.CTkLabel(master=Form1, text="")
VideoFeed.place(relx=0.5, rely=0.5, anchor="center")
# tkRender(ctk,VideoFeed, "Video.png",0.5)

def button_function():
    pass

Login_Button = ctk.CTkButton(master=Form1, font=font1, text="LOGIN", command=button_function, height=50, width=300,
                             fg_color=("black","yellow"), text_color=("white","black"), corner_radius=10,hover_color="white")
Login_Button.place(relx=0.5, rely=0.4, anchor="center")


Register_Button = ctk.CTkButton(master=Form1, font=font1, text="REGISTER", command=button_function, height=50, width=300,
                                fg_color=("black","yellow"), text_color=("white","black"), corner_radius=10,hover_color="white")
Register_Button.place(relx=0.5, rely=0.6, anchor="center")

app.after(5, MainLoop)
app.mainloop()