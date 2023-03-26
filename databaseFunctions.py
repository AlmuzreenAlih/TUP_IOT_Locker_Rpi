import sqlite3
import time

db = sqlite3.connect("lockerdb.db", check_same_thread=False)
class DB_InsertC:
    def __init__(self):
        self.ToAdd = []
        self.stmt = ""
        self.db = None
        self.table = ""
    def Init(self, db,table):
        self.db = db
        self.table = table
    def Add(self, arr):
        if len(arr) == 2:
            self.ToAdd.append(arr)
        else:
            print("Wrong Format")
    def Commit(self):
        fields = ''
        values = ''
        for i in self.ToAdd:
            fields = fields + '"' + i[0] + '",'
            values = values + '"' + i[1] + '",'
        self.stmt = 'INSERT INTO "main"."' + self.table + '"(' + fields[0:-1] + ')'\
                'VALUES (' + values[0:-1] + ');'
        print(self.stmt)
        cur = self.db.cursor()
        cur.execute(self.stmt)
        self.db.commit()
        self.ToAdd = []
        self.stmt = ""

class DB_UpdaterC:
    def __init__(self):
        self.ToAdd = []
        self.stmt = ""
        self.db = None
        self.table = ""
    def Init(self, db,table):
        self.db = db
        self.table = table
    def Add(self, arr):
        if len(arr) == 2:
            self.ToAdd.append(arr)
        else:
            print("Wrong Format")
    def Commit(self,WHERE, ID):
        setting = ""
        for i in self.ToAdd:
            setting = setting + i[0] + "='" + str(i[1]) +"'," 
        self.stmt = 'UPDATE ' + self.table + " SET " + setting[0:-1] + " WHERE " + WHERE + "='" + str(ID) +"'"
        
        print(self.stmt)
        cur = self.db.cursor()
        cur.execute(self.stmt)
        self.db.commit()
        self.ToAdd = []
        self.stmt = ""

def DB_Selector(db, table, WHERE, ID, additional=None):
    cur = db.cursor()
    stmt = "SELECT * FROM " + table + " WHERE " + WHERE + " = " + str(ID) + ";"
    if additional is not None:
        stmt = stmt[0:-1] + " " + additional + ";"
    print(stmt)
    cur.execute(stmt)
    rows = cur.fetchall()
    return rows

def DB_SelectAll(db, table):
    cur = db.cursor()
    stmt = "SELECT * FROM " + table
    print(stmt)
    cur.execute(stmt)
    rows = cur.fetchall()
    return rows

def DB_Deleter(db, table, WHERE, ID,All=False):
    cur = db.cursor()
    if All == False:
        stmt = "DELETE FROM " + table + " WHERE " + WHERE + " = " + str(ID) + ";"
    else:
        stmt = "DELETE FROM " + table + " WHERE " + WHERE + " = " + str(ID) + ";"

    print(stmt)
    cur.execute(stmt)
    db.commit()

def Examples():
    DB_Insert = DB_InsertC()
    DB_Updater = DB_UpdaterC()
    #################### Inserter ##########################    
    DB_Insert.Init(db=db, table="records")
    DB_Insert.Add(["guest_id","4"])
    DB_Insert.Add(["room_id","4"])
    DB_Insert.Add(["Action","4"])
    DB_Insert.Commit()

    #################### UPDATER ###########################
    DB_Updater.Init(db=db, table="guests")
    DB_Updater.Add(["name","fn"])
    DB_Updater.Add(["email","em"])
    DB_Updater.Add(["contact_number","pn"])
    DB_Updater.Add(["status",2])
    DB_Updater.Commit(WHERE="id", ID=1)


    #################### SELECTOR ###########################
    GuestA = DB_Selector(db=db, table="guests", WHERE="id ", ID=2)
    print(GuestA)

    #################### DELETER ###########################
    DB_Deleter(db=db, table="guests", WHERE="id ", ID=2, All=False)
    DB_Deleter(db=db, table="records", WHERE="guest_id ", ID=1, All=True)