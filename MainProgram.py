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

##################################################### GUI1 #####################################################################################
CropWidth = 250
CropHeight = 250
Steady = 0
Captured = 0
Process = 0
def MainLoop():
    global Process
    global All, AllLockers,  lockerChosen, Uid_of_the_user
    # print(time.time(), Process)
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
        delay = 4
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
            tkRender(ctk,VideoFeed,"Video.png",0.45)

        else:
            Steady, Captured = 0, 1
            cv2.imwrite("Video.png", cropped)
            tkRender(ctk,VideoFeed,"Video.png",0.9)
            Status_label.configure(text='Press "R" to retake picture.')
            Process = 0
    elif Process == 2:
        f = open("filename.txt", "r+")
        reading = f.read()
        f.close()
        time.sleep(0.3)
        ###reading = SerialData.read().decode("utf-8")
        if reading == 'A':
            FingerPrintStatus.configure(text="Remove Finger")
            WriteFile()
        elif reading == 'Y':
            FingerPrintStatus.configure(text="Place your finger again")
            WriteFile()
        elif reading == 'B':
            FingerPrintStatus.configure(text="User Successfully registered")
            WriteFile()
            app.after(3000, Success1)
        elif reading == 'X':
            FingerPrintStatus.configure(text="Try again")
            WriteFile()
        elif reading == 'Z':
            FingerPrintStatus.configure(text="Error Occured")
            WriteFile()
            app.after(3000, Error1)
        print(reading)
    elif Process==0.1 or Process==0.2:
        f = open("filename.txt", "r+")
        reading = f.read()
        f.close()
        WriteFile()
        ###reading = SerialData.read().decode("utf-8")
        
        if Process==0.1:
            if reading != "":
                User = DB_Selector(db=db, table="users", WHERE="finger_id ", ID=str(int(reading)))
                if len(User) > 0:
                    User = User[0]
                    Uid_of_the_user = User[0]
                    print(User)
                    TimedLogic = User[7]
                    R_Date = User[2]
                    if TimedLogic == 0:
                        print("Success101") #Make a checker instead
                        # if time.time() - int(R_Date) > 24*60*60:
                        #     messagebox.showerror('Error', 'You were registered not today')
                        # else:
                        #     Process=0.11
                        #     tkHide(FingerPrintPanel2)
                        Process=0.11
                        tkHide(FingerPrintPanel2)
                    else:
                        messagebox.showerror('Error', 'Already timed in to a different locker')
                        Process=0
                        tkHide(GUI4)
                        tkPack(GUI1)
                        tkHide(FingerPrintPanel2)
                else:
                    messagebox.showerror('Error', 'User Not defined')
                    Process=0
                    tkHide(GUI4)
                    tkPack(GUI1)
                    tkHide(FingerPrintPanel2)
        if Process==0.2:            
            if reading != "":
                logg = DB_Selector(db=db, table="logs", WHERE="locker ", ID=lockerChosen, additional="ORDER BY id ASC")[-1]
                S_Time = logg[1]
                T_Allowance = logg[2]
                Uid = logg[4]
                finger_id = DB_Selector(db=db, table="users", WHERE="id ", ID=Uid)[0][1]
                if int(finger_id) == int(reading):
                    Process = 0.21
                    tkHide(FingerPrintPanel2)
                else:
                    messagebox.showerror('Error', 'Invalid finger Id for the locker')
    elif Process==0.11 or Process==0.21:
        if Process==0.11:
            _, capt = cap.read()
            height, width, _ = capt.shape
            left, top = int((width - CropWidth) / 2), int((height - CropHeight) / 2)
            right, bottom = left + CropWidth, top + CropHeight
            cropped = capt[top:bottom, left:right]
            cv2.imwrite("compare.png",cropped)
            tkRender(ctk, VideoFeed2, "compare.png",0.68)
            known_image = face_recognition.load_image_file("Images/" + str(Uid_of_the_user)+".png")
            unknown_image = face_recognition.load_image_file("compare.png")
            biden_encoding = face_recognition.face_encodings(known_image)[0]

            try:
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]        
                results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
            except:
                results = False
            
            if results:
                DB_Updater.Init(db=db, table="users")
                DB_Updater.Add(["timed",str(1)])
                DB_Updater.Commit(WHERE="id", ID=str(Uid_of_the_user))
                
                DB_Updater.Init(db=db, table="lockers")
                DB_Updater.Add(["availability",str(1)])
                DB_Updater.Commit(WHERE="id", ID=str(lockerChosen))
                
                DB_Insert.Init(db=db, table="logs")
                Time_now = str(int(time.time()))
                DB_Insert.Add(["start_time",Time_now])
                DB_Insert.Add(["time_allowance",str(4*60*60)])
                DB_Insert.Add(["locker",str(lockerChosen)])
                DB_Insert.Add(["user_id",str(Uid_of_the_user)])
                DB_Insert.Commit() 
                
                Process=0
                tkHide(GUI4)
                tkPack(GUI1)
                tkHide(FingerPrintPanel2)
        if Process==0.21:
            logg = DB_Selector(db=db, table="logs", WHERE="locker ", ID=lockerChosen, additional="ORDER BY id ASC")[-1]
            S_Time = logg[1]
            T_Allowance = logg[2]
            Uid = logg[4]
            finger_id = DB_Selector(db=db, table="users", WHERE="id ", ID=Uid)[0][1]
            
            _, capt = cap.read()
            height, width, _ = capt.shape
            left, top = int((width - CropWidth) / 2), int((height - CropHeight) / 2)
            right, bottom = left + CropWidth, top + CropHeight
            cropped = capt[top:bottom, left:right]
            cv2.imwrite("compare.png",cropped)
            tkRender(ctk, VideoFeed2, "compare.png",0.68)
            known_image = face_recognition.load_image_file("Images/" + str(Uid)+".png")
            unknown_image = face_recognition.load_image_file("compare.png")
            biden_encoding = face_recognition.face_encodings(known_image)[0]
            try:
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]        
                results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
            except:
                results = False
            global Needed
            if results:
                T_Elapsed = time.time() - S_Time
                # if T_Elapsed > T_Allowance and T_Elapsed < T_Allowance + 3*24*60*60:
                #     T_Required = T_Elapsed - T_Allowance
                #     T_Required = T_Required/3600
                    
                #     Needed_Time = int(T_Required)+1
                    
                #     ans = messagebox.askyesno("Error","Locked in, unless you pay fine of"+ str(Needed_Time) + " hours.")
                #     if ans == "yes":
                #         tkHide(GUI3)
                #         tkPack(GUI5)
                #     else:
                #         pass
                # # elif T_Elapsed > T_Allowance + 3*24*60*60:
                # else:
                if True:
                    if (T_Elapsed > T_Allowance + 3*24*60*60):
                        print("Will be Timed out with penalty") #f3f
                    else:
                        print("Will be Timed out normally")
                    All_Time_Logs = len(DB_Selector(db=db, table="logs", WHERE="user_id ", ID=Uid))
                    Membership_Time = time.time() - DB_Selector(db=db, table="users", WHERE="id ", ID=Uid)[0][2]
                    Membership_Time = Membership_Time/(60*60) # This is in hours
                    Process = 0
                    tkHide(FingerPrintPanel2)
                    tkHide(GUI4)
                    tkPack(GUI1)
                    # if All_Time_Logs == 1 and Membership_Time > 24:
                    print(time.time() - DB_Selector(db=db, table="users", WHERE="id ", ID=Uid)[0][2],Membership_Time)
                    if Membership_Time > 24 or All_Time_Logs == 2:                        
                        finger_id = int(finger_id)
                        finger_id = -finger_id
                        
                        DB_Updater.Init(db=db, table="users")
                        DB_Updater.Add(["finger_id",str(finger_id)])
                        DB_Updater.Add(["timed",str(0)])
                        DB_Updater.Commit(WHERE="id", ID=str(Uid))
                        
                        DB_Updater.Init(db=db, table="lockers")
                        DB_Updater.Add(["availability",str(0)])
                        DB_Updater.Commit(WHERE="id", ID=str(lockerChosen))
                        if Membership_Time > 24:
                            messagebox.showinfo('Success', 'You will be deleted to the database, since > 24 hrs')
                            print("")
                        if All_Time_Logs == 2:
                            messagebox.showinfo('Success', 'You will be deleted to the database, you had 2 trials already')
                    elif Membership_Time < 24:
                        DB_Updater.Init(db=db, table="users")
                        DB_Updater.Add(["timed",str(0)])
                        DB_Updater.Commit(WHERE="id", ID=str(Uid))
                        
                        DB_Updater.Init(db=db, table="lockers")
                        DB_Updater.Add(["availability",str(0)])
                        DB_Updater.Commit(WHERE="id", ID=str(lockerChosen))
                        messagebox.showinfo('Success', 'You still have 1 trial for today.')
            else:
                messagebox.showerror('Error', 'Image Identity did not match.')
    elif Process==0.3:
        global Inserted
        f = open("filename.txt", "r+")
        reading = f.read()
        f.close()
        WriteFile()
        ###reading = SerialData.read().decode("utf-8")
        
        if reading != "":
            if reading == "a":
                Inserted = Inserted + 5
            elif reading == "b":
                Inserted = Inserted + 20
            elif reading == "c":
                Inserted = Inserted + 50
            elif reading == "d":
                Inserted = Inserted + 100
            elif reading == "e":
                Inserted = Inserted + 200
            elif reading == "f":
                Inserted = Inserted + 500
            elif reading == "g":
                Inserted = Inserted + 1000
            elif reading == "h":
                Inserted = Inserted + 5000
            AcceptedLabel.configure(text="Inserted money: " + str(Inserted) + " (" + str(int(Inserted/5)) + " hrs)")
    app.after(5,MainLoop)

GUI1 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
GUI1.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI1, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkRender(ctk,bg,"logo2.png",1)

def Lockers_Button_function():
    global Process; Process = 0
    tkPack(GUI3); tkHide(GUI1)
    resetGUI2(); resetButtons()

Lockers_Button = ctk.CTkButton(master=GUI1, font=font0, text="CHOOSE LOCKER", command=Lockers_Button_function, height=80, width=500,
                             fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
Lockers_Button.place(relx=0.06, rely=0.16, anchor="nw")

# Logout_Button = ctk.CTkButton(master=GUI1, font=font0, text="TIME OUT", command=button_function, height=80, width=500,
#                              fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
# Logout_Button.place(relx=0.5, rely=0.5, anchor="center")

def Register_Button_Function():
    global Process; Process = 1
    tkPack(GUI2); tkHide(GUI1)
    resetGUI2(); resetButtons()
    
Register_Button = ctk.CTkButton(master=GUI1, font=font0, text="REGISTER", command=Register_Button_Function, height=80, width=500,
                                fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
Register_Button.place(relx=0.32, rely=0.67, anchor="nw")

########################################## GUI2 ##########################################################################
def WriteFile():
    f = open("filename.txt", "w+")
    f.write("") 
    f.close()

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
    DB_Insert.Add(["reg_date",str(time.time())])
    DB_Insert.Add(["timed",str(1)])
    DB_Insert.Commit()    
    copy("Cropped.png", "Images", str(DB_SelectAll(db=db,table="users")[-1][0]) + ".png")
    
    tkHide(FingerPrintPanel)
    tkPack(GUI3)
    tkHide(GUI2)
    FingerPrintStatus.configure(text="Put your finger on the reader.")
    Name1Entry.delete(0,-1)
    Name2Entry.delete(0,-1)
    Name3Entry.delete(0,-1)
    ContactEntry.delete(0,-1)

GUI2 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
# GUI2.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI2, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkRender(ctk,bg,"bg2.png",1)

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
# tkRender(ctk,VideoFeed, "Video.png",0.5)

Status_label = ctk.CTkLabel(master=GUI2, font=font1, text="Center your face within the box.", fg_color="white")
Status_label.place(relx=0.8, rely=0.60, anchor="n")
    
def Error1():
    FingerPrintStatus.configure(text="Put your finger on the reader.")

def GetAll():
    global All, AllLockers
    All = DB_SelectAll(db=db, table="users")
    # AllLocker = DB_SelectAll(db=db, table="lockers")
    # dummy = 1677576153
    # AllLockers = []
    # for Locker in AllLocker:
    #     StartTime = DB_Selector(db=db, table="logs", WHERE="locker", ID=Locker[0])[1]
    #     TimeAllowance = DB_Selector(db=db, table="logs", WHERE="locker", ID=Locker[0])[2]
    #     RemainingTime = TimeAllowance - (time.time() - StartTime)
        
GetAll()

def GetLeastAvailable():
    global All
    list1 = []
    for a in All:
        list1.append(a[1])
    return GetLeastAvailable2(list1)

def GetLeastAvailable2(lst):
    # Create a set containing all numbers from 0 to 127
    all_numbers = set(range(128))
    
    # Remove numbers that are present in lst
    for num in lst:
        all_numbers.discard(num)
    
    # Find the smallest remaining number
    least_available = min(all_numbers)
    
    # Return the result
    return least_available

print(GetLeastAvailable())
def Proceed_Button1_Func():
    global Captured, Process
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
            Process = 2

Proceed_Button1 = ctk.CTkButton(master=GUI2, font=font1, text="SUBMIT", command=Proceed_Button1_Func, height=37, width=150,
                             fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Proceed_Button1.place(relx=0.575, rely=0.56, anchor="ne")

Back_Button1 = ctk.CTkButton(master=GUI2, font=font1, text="BACK", command=Proceed_Button1_Func, height=37, width=150,
                             fg_color="red", text_color=("white","black"), corner_radius=10,hover_color="orange")
Back_Button1.place(relx=0.05, rely=0.56, anchor="nw")

FingerPrintPanel = ctk.CTkFrame(master=GUI2, width=600, height=290, fg_color="gray85", corner_radius=9, border_width=2)
# FingerPrintPanel.place(relx=0.5, rely=0.5, anchor="center")

FingerPrintImg = ctk.CTkLabel(master=FingerPrintPanel, text="", width=100, height=100, fg_color="gray40", corner_radius=9)
FingerPrintImg.place(relx=0.1, rely=0.5, anchor="w")
tkRender(ctk, FingerPrintImg, "f1.png", 0.25)

FingerPrintStatus = ctk.CTkLabel(master=FingerPrintPanel, font=font1, text="Please put your finger on the reader.", corner_radius=9)
FingerPrintStatus.place(relx=0.35, rely=0.5, anchor="w")

#########################################################################################################################################

GUI3 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
# GUI3.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI3, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkRender(ctk,bg,"bg2.png",1)

def resetButtons():
    for i in GUI3.winfo_children():
        if isinstance(i, ctk.CTkButton) and i.cget("text").isdecimal():
            i.configure(fg_color="#c4203c")
def resetGUI2():
    Timein_Button.place_forget()
    Timeout_Button.place_forget()
    Extend_Button.place_forget()
    
def print_button_number(button_number):
    global Process, lockerChosen
    resetButtons()
    for i in GUI3.winfo_children():
        if isinstance(i, ctk.CTkButton) and i.cget("text")==str(button_number):
            i.configure(fg_color="green")
    if Process == 2:
        lockerChosen = button_number
        id = DB_SelectAll(db=db, table="users")[-1][0]
        DB_Insert.Init(db=db, table="logs")
        Time_now = str(int(time.time()))
        DB_Insert.Add(["start_time",Time_now])
        DB_Insert.Add(["time_allowance",str(4*60*60)])
        DB_Insert.Add(["locker",str(lockerChosen)])
        DB_Insert.Add(["user_id",str(id)])
        DB_Insert.Commit()    
        
        DB_Updater.Init(db=db, table="lockers")
        DB_Updater.Add(["availability",str(1)])
        DB_Updater.Commit(WHERE="id", ID=str(lockerChosen))
        
        DB_Updater.Init(db=db, table="users")
        DB_Updater.Add(["reg_date",Time_now])
        DB_Updater.Commit(WHERE="id", ID=id)
        tkHide(GUI3)
        tkPack(GUI1)
    elif Process == 0:
        lockerChosen = button_number
        Timein_Button.place(relx=0.6, rely=0.225, anchor="nw")
        Timeout_Button.place(relx=0.6, rely=0.415, anchor="nw")
        Extend_Button.place(relx=0.6, rely=0.605, anchor="nw")
        
def Timein_Button_Function():
    global lockerChosen, Process
    print("Chosen Locker:", lockerChosen)
    availability = DB_Selector(db=db, table="lockers", WHERE="id ", ID=lockerChosen)[0][1]
    if availability == 0: #available or not occupied
        Process = 0.1
        tkHide(GUI3)
        tkPack(GUI4) 
        FingerPrintPanel2.place(relx=0.5, rely=0.5, anchor="center")    
    else:
        messagebox.showerror('Error', 'Someone is timed in here')

def Timeout_Button_Function():
    global lockerChosen, Process, Needed_Time, NeededMoney, log_id, T_Allowance, Extending_Mode
    print("Chosen Locker:", lockerChosen)
    availability = DB_Selector(db=db, table="lockers", WHERE="id ", ID=lockerChosen)[0][1]
    if availability == 1: #Not available or occupied
        logg = DB_Selector(db=db, table="logs", WHERE="locker ", ID=lockerChosen, additional="ORDER BY id ASC")[-1]
        log_id = logg[0]
        S_Time = logg[1]
        T_Allowance = logg[2]
        Uidd = logg[4]
        
        T_Elapsed = time.time() - S_Time
        if T_Elapsed > T_Allowance and T_Elapsed < T_Allowance + 3*24*60*60:
            T_Required = T_Elapsed - T_Allowance
            T_Required = T_Required/3600
            
            Needed_Time = int(T_Required)+1
            NeededMoney = Needed_Time*5
            ans = messagebox.askyesno("Error","Locked in, unless you pay fine of"+ str(Needed_Time) + " hours.")
            print(repr(ans))
            if ans == True:
                Process = 0.3
                Extending_Mode = 1
                tkHide(GUI3)
                tkPack(GUI5)
                NeededLabel.configure(text="Needed money: ₱" + str(NeededMoney) + " (" + str(Needed_Time) + "hrs)")
            else:
                pass
        else:
            Process = 0.2
            tkHide(GUI3)
            tkPack(GUI4) 
        FingerPrintPanel2.place(relx=0.5, rely=0.5, anchor="center")    
    else:
        messagebox.showerror('Error', 'No one is timed in here.')
  
def Extend_Button_Function():
    global lockerChosen, Process, Extending_Mode, log_id
    print("Chosen Locker:", lockerChosen)
    availability = DB_Selector(db=db, table="lockers", WHERE="id ", ID=lockerChosen)[0][1]
    logg = DB_Selector(db=db, table="logs", WHERE="locker ", ID=lockerChosen, additional="ORDER BY id ASC")[-1]
    
    if availability == 1: #Not available or occupied
        Process = 0.3
        Extending_Mode = 2
        log_id = logg[0]
        tkHide(GUI3)
        tkPack(GUI5) 
        FingerPrintPanel2.place(relx=0.5, rely=0.5, anchor="center")    
    else:
        messagebox.showerror('Error', 'No one is timed in here.')

Timein_Button = ctk.CTkButton(master=GUI3, font=font0, text="TIME IN", command=Timein_Button_Function, height=50, width=250,
                                fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
# Timein_Button.place(relx=0.6, rely=0.23, anchor="nw")  
  
Timeout_Button = ctk.CTkButton(master=GUI3, font=font0, text="TIME OUT", command=Timeout_Button_Function, height=50, width=250,
                                fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
# Timeout_Button.place(relx=0.6, rely=0.42, anchor="nw")

Extend_Button = ctk.CTkButton(master=GUI3, font=font0, text="EXTEND", command=Extend_Button_Function, height=50, width=250,
                                fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
# Extend_Button.place(relx=0.6, rely=0.42, anchor="nw")

for i in range(1, 16):
    row = (i-1) // 3
    col = (i-1) % 3
    button = ctk.CTkButton(master=GUI3, font=font0, text=str(i), width=100, height=60, corner_radius=10,
                           command=lambda button_number=i: print_button_number(button_number), fg_color="#c4203c")
    button.place(relx=(0.2 * col) + 0.1, rely=(0.19 * row) + 0.1, anchor="center")
    
    Time_label = ctk.CTkLabel(master=GUI3, font=font1, text="00:00:00", fg_color="white")
    Time_label.place(relx=(0.2 * col) + 0.1, rely=(0.19 * row) + 0.195, anchor="center")
    9
#########################################################################################################################################

GUI4 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
# GUI4.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI4, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkRender(ctk,bg,"bg2.png",1)

def MainLoop2():
    f = open("filename.txt", "r+")
    reading = f.read()
    f.close()
    ###reading = SerialData.read().decode("utf-8")
    
    app.after(5,MainLoop2)

VideoFeed2 = ctk.CTkLabel(master=GUI4, text="")
VideoFeed2.place(relx=0.5, rely=0.5, anchor="center")

FingerPrintPanel2 = ctk.CTkFrame(master=GUI4, width=600, height=290, fg_color="gray85", corner_radius=9, border_width=2)
# FingerPrintPanel2.place(relx=0.5, rely=0.5, anchor="center")

FingerPrintImg2 = ctk.CTkLabel(master=FingerPrintPanel2, text="", width=100, height=100, fg_color="gray40", corner_radius=9)
FingerPrintImg2.place(relx=0.1, rely=0.5, anchor="w")
tkRender(ctk, FingerPrintImg2, "f1.png", 0.25)

FingerPrintStatus2 = ctk.CTkLabel(master=FingerPrintPanel2, font=font1, text="Please put your finger on the reader.", corner_radius=9)
FingerPrintStatus2.place(relx=0.35, rely=0.5, anchor="w")


#########################################################################################################################################

GUI5 = ctk.CTkFrame(master=app, width=800, height=480, fg_color="transparent", corner_radius=0)
# GUI5.place(relx=0.5, rely=0.5, anchor="center")
bg = ctk.CTkLabel(master=GUI5, text="")
bg.place(relx=0.5, rely=0.5, anchor="center")
tkRender(ctk,bg,"bg2.png",1)

AcceptorPanel2 = ctk.CTkFrame(master=GUI5, width=600, height=290, fg_color="gray85", corner_radius=9, border_width=2)
AcceptorPanel2.place(relx=0.5, rely=0.5, anchor="center")

AcceptorImg2 = ctk.CTkLabel(master=AcceptorPanel2, text="", width=100, height=100, fg_color="gray40", corner_radius=9)
AcceptorImg2.place(relx=0.1, rely=0.5, anchor="w")
tkRender(ctk, AcceptorImg2, "f1.png", 0.25)

AcceptorStatus2 = ctk.CTkLabel(master=AcceptorPanel2, font=font1, text="Insert coins or bills. (₱5.00/hr)", corner_radius=9)
AcceptorStatus2.place(relx=0.35, rely=0.4, anchor="w")

Inserted = 0
Needed = 0

def resetAccepted():
    AcceptedLabel.configure(text="Inserted money: ₱0.00")
    NeededLabel.configure(text="Needed money: ₱0.00")

AcceptedLabel = ctk.CTkLabel(master=AcceptorPanel2, font=font1, text="", corner_radius=9)
AcceptedLabel.place(relx=0.35, rely=0.6, anchor="w")

NeededLabel = ctk.CTkLabel(master=AcceptorPanel2, font=font1, text="", corner_radius=9)
NeededLabel.place(relx=0.35, rely=0.7, anchor="w")

def Cancel_Function5():
    tkHide(GUI5)
    tkPack(GUI1)
def Proceed_Function5():
    global NeededMoney, Inserted, log_id, Extending_Mode, Process
    if Extending_Mode == 1:
        if Inserted > NeededMoney:
            tkHide(GUI5)
            tkPack(GUI1)
            resetAccepted()
        else:
            ans = messagebox.askokcancel('Error', 'Inserted Money is not enough. If you press "Ok", you will still NOT be timed out.')
            if ans == True:
                Time_Allowance = DB_Selector(db=db, table="logs", WHERE="id ", ID=str(log_id))[0][2]
    
                DB_Updater.Init(db=db, table="logs")
                DB_Updater.Add(["time_allowance",str(Time_Allowance + (Inserted/5)*60*60)])
                DB_Updater.Commit(WHERE="id", ID=log_id)
                resetAccepted()
            else:
                pass
    if Extending_Mode == 2:
        Time_Allowance = DB_Selector(db=db, table="logs", WHERE="id ", ID=str(log_id))[0][2]
        
        DB_Updater.Init(db=db, table="logs")
        DB_Updater.Add(["time_allowance",str(Time_Allowance + (Inserted/5)*60*60)])
        DB_Updater.Commit(WHERE="id", ID=log_id)
        messagebox.showinfo("Success", "Time extension is successful")
        Process = 0
        tkHide(GUI5)
        tkPack(GUI1)
        resetAccepted()
        

Cancel5_Button = ctk.CTkButton(master=GUI5, font=font1, text="CANCEL", command=Cancel_Function5, height=30, width=150,
                                fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
Cancel5_Button.place(relx=0.12, rely=0.85, anchor="nw")  

Proceed5_Button = ctk.CTkButton(master=GUI5, font=font1, text="SUBMIT", command=Proceed_Function5, height=30, width=150,
                                fg_color="#c4203c", text_color=("white","black"), corner_radius=10,hover_color="orange")
Proceed5_Button.place(relx=0.7, rely=0.85, anchor="nw")  

resetAccepted()

def key_input(event):
    if event.char == "`":
        app.after(5, MainLoop)

# Lockers_Button_function()
app.after(5,MainLoop)
app.bind("<KeyPress>", key_input)
app.mainloop()