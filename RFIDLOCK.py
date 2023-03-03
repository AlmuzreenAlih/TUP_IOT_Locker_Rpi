import random
import sqlite3
import time
import threading
import eel
import keyboard
import serial
import ImportantFunctions as IF
# SerialData = serial.Serial("/dev/ttyUSB0", 9600, timeout = 0.2)
SerialData = serial.Serial("com3", 9600, timeout = 0.2)
SerialData.setDTR(False)
time.sleep(1)
SerialData.flushInput()
SerialData.setDTR(True)
time.sleep(2)
# SerialData.write(bytes("2", "utf-8"))
# reading = SerialData.readline().decode("utf-8")
# reading = SerialData.readline().decode("utf-8")
#	 if reading == 'A':
#		 pass
    
class InsertThis:
    def __init__(self):
        self.ToAdd = []
        self.stmt = ""
    
    def Add(self, arr):
        if len(arr) == 2:
            self.ToAdd.append(arr)
        else:
            print("Wrong Format")
    def PrepareStmt(self, table):
        fields = ''
        values = ''
        for i in self.ToAdd:
            fields = fields + '"' + i[0] + '",'
            values = values + '"' + i[1] + '",'
        self.stmt = 'INSERT INTO "main"."' + table + '"(' + fields[0:-1] + ')'\
                'VALUES (' + values[0:-1] + ');'
        print(self.stmt)
        return self.stmt
    
    def ClearThis(self):
        self.ToAdd = []
        self.stmt = ""
        
class UpdateThis:
    def __init__(self):
        self.ToAdd = []
        self.stmt = ""
        self.fieldID = ""
        self.ID = ""
    
    def Add(self, arr):
        if len(arr) == 2:
            self.ToAdd.append(arr)
        else:
            print("Wrong Format")
    def PrepareStmt(self, table, fieldID, ID):
        setting = ""
        self.fieldID = fieldID
        self.ID = ID
        for i in self.ToAdd:
            setting = setting + i[0] + "='" + i[1] +"'," 
        self.stmt = 'UPDATE ' + table + " SET " + setting[0:-1] + " WHERE " + fieldID + "='" + ID +"'"
        print(self.stmt)
        return self.stmt
    
    def ClearThis(self):
        self.ToAdd = []
        self.stmt = ""
        self.fieldID = ""
        self.ID = ""
        

eel.init('GUI')

db = sqlite3.connect("RFID_Database.db", check_same_thread=False)

def GetAdminInfo():
    global db
    cur = db.cursor()
    cur.execute("SELECT * FROM user ORDER by _rowid_")
    rows = cur.fetchall()
    return rows[0]

def GetAllRooms():
    global db
    cur = db.cursor()
    cur.execute("SELECT * FROM rooms ORDER by _rowid_")
    rows = cur.fetchall()
    return rows

def GetAllGuests():
    global db
    cur = db.cursor()
    cur.execute("SELECT * FROM guests ORDER by _rowid_")
    rows = cur.fetchall()
    return rows

def Get_Guest_Records(id):
    global db
    cur = db.cursor()
    stmt = "SELECT * FROM records WHERE guest_id = " + str(id)
    print(stmt)
    cur.execute(stmt)
    rows = cur.fetchall()
    return rows

def GET_S(Table, ID, Is):
    global db
    cur = db.cursor()
    stmt = "SELECT * FROM " + Table + " WHERE " + ID + " = " + str(Is) + ";"
    print(stmt)
    cur.execute(stmt)
    rows = cur.fetchall()
    return rows

def UPDATE_S(Table, Field, Value, ID, Is):
    global db
    cur = db.cursor()
    stmt = "UPDATE " + Table + " SET " + Field + " = '" + str(Value) + "' WHERE " + ID + " = " + str(Is) + ";"
    print(stmt)
    cur.execute(stmt)
    db.commit()

def EXECUTE(stmt):
    global db
    cur = db.cursor()
    print(stmt)
    cur.execute(stmt)
    db.commit()

AdminInfos = GetAdminInfo()

Name = AdminInfos[0] #"John Jose de la Cruz"
Email = AdminInfos[1] #"jjdlc1960@gmail.com"
Number = AdminInfos[2] #"0990991811"
Username = AdminInfos[3] # "adminjj"
Password = AdminInfos[4] #"admindlc"
AdminInfo= [Name,Email,Number,Username,Password]

InsertThis1 = InsertThis()
UpdateThis1 = UpdateThis()

def GetGuestOfRoom(id):
    global db
    cur = db.cursor()
    stmt = "SELECT * FROM guests WHERE room = " + str(id)
    print(stmt)
    cur.execute(stmt)
    rows = cur.fetchall()
    return rows

def divide(string, N):
    # Initialize a list to store the divisions
    divisions = []

    # Divide the string into separate parts
    for i in range(0, len(string), N):
        divisions.append(string[i:i+N])

    return divisions



def MainLoop():
    global x, reading, debug, RegisterMode, AdminInfo
    reading = ""
    reading = SerialData.readline().decode("utf-8")
    # if keyboard.is_pressed('z'):
    #     reading = random.choice(["A25464564,1B"]) #,"A25464564,1B","A35476987,1B","A41435879,1B","A5123476986,1B","A61235428,2B"
    # if keyboard.is_pressed('x'):
    #     reading = random.choice(["A35476987,1B"])
    # if keyboard.is_pressed('space'):
    #     reading = random.choice(["A1B"])
        
    # print(reading)
    if (len(reading)>2):
        Parsed = IF.GetINFO(reading,"A","B")
        try:
            RFID_Reading = Parsed.split(",")[0]
            Room_id = Parsed.split(",")[1]
            Registered_guest = GetGuestOfRoom(Room_id)
        except:
            RFID_Reading = ""
            Room_id = Parsed
            Registered_guest = GetGuestOfRoom(Room_id)
        
        # print(Parsed,RFID_Reading,Room_id,Registered_guest)
        if len(Registered_guest) > 0:
            # print(repr(Registered_guest[0][8]),repr(RFID_Reading))
            if RFID_Reading == Registered_guest[0][8]:
                eel.RFID_Read(RFID_Reading + " " + str(Registered_guest[0][1]) + " of room id = " + str(Room_id) + " RFID Accept")
                SerialData.write(bytes("1", "utf-8"))
                time.sleep(5)
                
                if RegisterMode == 0:
                    InsertThis1.Add(["guest_id",str(Registered_guest[0][0])])
                    InsertThis1.Add(["room_id",str(Room_id)])
                    InsertThis1.Add(["action","Time In"])
                    InsertThis1.Add(["timestamp",str(int(time.time()))])
                    EXECUTE(InsertThis1.PrepareStmt(table="records"))
                    InsertThis1.ClearThis()
                    stringToSend = "!"+str(Registered_guest[0][12])+"@Hello "+str(Registered_guest[0][11]) + ","+str(Registered_guest[0][1]) + " timed in the room@_"
                    for i in divide(stringToSend,20):
                        print(i)
                        SerialData.write(bytes(i, "utf-8"))
                        time.sleep(0.5)
            elif len(Parsed) < 7:
                eel.RFID_Read(RFID_Reading + " " + str(Registered_guest[0][1]) + " of room id = " + (Room_id) + " RFID Accept")
                SerialData.write(bytes("1", "utf-8"))
                time.sleep(5)
                
                if RegisterMode == 0:
                    InsertThis1.Add(["guest_id",str(Registered_guest[0][0])])
                    InsertThis1.Add(["room_id",str(Room_id)])
                    InsertThis1.Add(["action","Time Out"])
                    InsertThis1.Add(["timestamp",str(int(time.time()))])
                    EXECUTE(InsertThis1.PrepareStmt(table="records"))
                    InsertThis1.ClearThis()
                    stringToSend = "!"+str(Registered_guest[0][12])+"@Hello "+str(Registered_guest[0][11]) + ","+str(Registered_guest[0][1]) + " timed out the room@_"
                    for i in divide(stringToSend,20):
                        print(i)
                        SerialData.write(bytes(i, "utf-8"))
                        time.sleep(0.5)
            else:
                SerialData.write(bytes("2", "utf-8"))
                eel.RFID_Read(RFID_Reading + " RFID Reject")
                if RegisterMode == 0:
                    time.sleep(1)
                    SerialData.write(bytes("!"+str(AdminInfo[2])+"@Hello "+str(AdminInfo[0]), "utf-8"))
                    time.sleep(2)
                    SerialData.write(bytes(",Someone enteres room id="+str(Room_id), "utf-8"))
                    time.sleep(2)
                    SerialData.write(bytes(" with an invalid card@_", "utf-8"))
                
        else:
            eel.RFID_Read(RFID_Reading + " RFID but room id = " + Room_id + " does not have a guest.")
            SerialData.write(bytes("2", "utf-8"))
            if RegisterMode == 0:
                time.sleep(1)
                SerialData.write(bytes("!"+str(AdminInfo[2])+"@Hello "+str(AdminInfo[0]), "utf-8"))
                time.sleep(2)
                SerialData.write(bytes(",Someone enteres room id="+str(Room_id), "utf-8"))
                time.sleep(2)
                SerialData.write(bytes(" with an invalid card@_", "utf-8"))
                        
    threading.Timer(0.1,MainLoop,[]).start()
    

MainLoop()
    
eel.JS_Display_Admin(Name,Email,Number,Username,Password)
eel.JS_SendRoomsAndGuests(GetAllRooms(),GetAllGuests())
eel.JS_DisplayRoomsAndGuests()
# eel.JS_Display_Guests(GetAllGuests())
# eel.JS_Display_Rooms(GetAllRooms())

#ROOMS
@eel.expose
def PY_Add_Room(na):
    InsertThis1.Add(["name",na])
    InsertThis1.Add(["status","0"])
    InsertThis1.Add(["guest_id","0"])
    InsertThis1.Add(["created_timestamp",str(int(time.time()))])
    EXECUTE(InsertThis1.PrepareStmt(table="rooms"))
    # eel.JS_Display_Rooms(GetAllRooms())
    # eel.JS_Display_Guests(GetAllGuests())
    eel.JS_SendRoomsAndGuests(GetAllRooms(),GetAllGuests())
    eel.JS_DisplayRoomsAndGuests()
    InsertThis1.ClearThis()
    
@eel.expose
def PY_Update_Room_Name(id,string):
    global Name,Email,Number,Username,Password
    print(id,string)
    UPDATE_S("rooms", "name", string ,"id ",id)
    # eel.JS_Display_Rooms(GetAllRooms())
    # eel.JS_Display_Guests(GetAllGuests())
    eel.JS_SendRoomsAndGuests(GetAllRooms(),GetAllGuests())
    eel.JS_DisplayRoomsAndGuests()
    
@eel.expose
def PY_Check_Out_Room(id):
    guest_id = GET_S("guests", "room ",str(id))[0][0]
    guest_id = str(guest_id)
    
    UPDATE_S("rooms","status","0","id ", id)
    UPDATE_S("rooms","guest_id","0","id ", id)
    UPDATE_S("guests","status","0","room ", id)
    UPDATE_S("guests","room","0","room ", id)
    
    InsertThis1.Add(["guest_id",str(guest_id)])
    InsertThis1.Add(["room_id",str(id)])
    InsertThis1.Add(["action","Check Out"])
    InsertThis1.Add(["timestamp",str(int(time.time()))])
    EXECUTE(InsertThis1.PrepareStmt(table="records"))
    InsertThis1.ClearThis()
    # eel.JS_Display_Rooms(GetAllRooms())
    # eel.JS_Display_Guests(GetAllGuests())
    eel.JS_SendRoomsAndGuests(GetAllRooms(),GetAllGuests())
    eel.JS_DisplayRoomsAndGuests()
    
@eel.expose
def PY_Check_In_Room(room_id, guest_name):
    guest_id = GET_S("guests", "name ","'"+guest_name+"'")[0][0]
    guest_id = str(guest_id)
    print(repr(guest_id))
    time.sleep(1)
    UPDATE_S("rooms","status","1","id ", room_id)
    UPDATE_S("rooms","guest_id",guest_id,"id ", room_id)
    UPDATE_S("guests","status","1","id ", guest_id)
    UPDATE_S("guests","room",room_id,"id ", guest_id)
    
    InsertThis1.Add(["guest_id",str(guest_id)])
    InsertThis1.Add(["room_id",str(room_id)])
    InsertThis1.Add(["action","Check In"])
    InsertThis1.Add(["timestamp",str(int(time.time()))])
    EXECUTE(InsertThis1.PrepareStmt(table="records"))
    InsertThis1.ClearThis()
    # eel.JS_Display_Rooms(GetAllRooms())
    # eel.JS_Display_Guests(GetAllGuests())
    eel.JS_SendRoomsAndGuests(GetAllRooms(),GetAllGuests())
    eel.JS_DisplayRoomsAndGuests()

#GUEST
@eel.expose
def PY_InsertGuest(fn,em,pn,ad,rf,pcnt,bthy, gec, gecn):
    InsertThis1.Add(["name",fn])
    InsertThis1.Add(["status","0"])
    InsertThis1.Add(["room","0"])
    InsertThis1.Add(["created_timestamp",str(int(time.time()))])
    InsertThis1.Add(["email",em])
    InsertThis1.Add(["contact_number",pn])
    InsertThis1.Add(["address",ad])
    InsertThis1.Add(["rfid",rf])
    InsertThis1.Add(["people",str(pcnt)])
    InsertThis1.Add(["birthday",str(bthy)])
    InsertThis1.Add(["emergency",str(gec)])
    InsertThis1.Add(["emergency_no",str(gecn)])
    EXECUTE(InsertThis1.PrepareStmt(table="guests"))
    # eel.JS_Display_Rooms(GetAllRooms())
    # eel.JS_Display_Guests(GetAllGuests())
    eel.JS_SendRoomsAndGuests(GetAllRooms(),GetAllGuests())
    eel.JS_DisplayRoomsAndGuests()
    InsertThis1.ClearThis()

@eel.expose
def PY_Save_Admin(na,em,nu,us,pa):
    global AdminNumber
    UpdateThis1.Add(["Name",na])
    UpdateThis1.Add(["Email",em])
    UpdateThis1.Add(["Number",nu])
    UpdateThis1.Add(["Username",us])
    UpdateThis1.Add(["Password",pa])
    EXECUTE(UpdateThis1.PrepareStmt(table="user",fieldID="id",ID="0"))
    UpdateThis1.ClearThis()
    AdminNumber = nu
    
    eel.JS_Display_Admin(na,em,nu,us,pa)

@eel.expose
def PY_UpdateGuest(id,fn,em,pn,ad,rf,pcnt,bthy,gec, gecn):
    UpdateThis1.Add(["name",fn])
    UpdateThis1.Add(["email",em])
    UpdateThis1.Add(["contact_number",pn])
    UpdateThis1.Add(["address",ad])
    UpdateThis1.Add(["rfid",rf])
    UpdateThis1.Add(["people",str(pcnt)])
    UpdateThis1.Add(["birthday",str(bthy)])
    UpdateThis1.Add(["emergency",str(gec)])
    UpdateThis1.Add(["emergency_no",str(gecn)])
    EXECUTE(UpdateThis1.PrepareStmt(table="guests",fieldID="id",ID=id))
    # eel.JS_Display_Rooms(GetAllRooms())
    # eel.JS_Display_Guests(GetAllGuests())
    eel.JS_SendRoomsAndGuests(GetAllRooms(),GetAllGuests())
    eel.JS_DisplayRoomsAndGuests()
    UpdateThis1.ClearThis()

@eel.expose
def PY_Get_Guest_Records(id):
    print("Records")
    eel.JS_Display_Records(Get_Guest_Records(id))

RegisterMode = 0
@eel.expose
def PY_Registering():
    global RegisterMode
    RegisterMode = 1
    SerialData.write(bytes("3", "utf-8"))
    print("Rego")
    
@eel.expose
def PY_Unregistering():
    global RegisterMode
    RegisterMode = 0
    SerialData.write(bytes("4", "utf-8"))
    

# # eel.start('index.html',geometry={'size': (200, 100), 'position': (0, 0)})
eel.start('index.html', mode='chrome', cmdline_args=['--start-maximized'])
# eel.start('index.html', mode='chrome', cmdline_args=['--kiosk'])