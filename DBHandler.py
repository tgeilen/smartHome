import sqlite3
import sqlite3
from datetime import datetime, time

from sre_constants import IN
from typing import List


class DBHandler:

    def __init__(self):

         
         

        self.conn = sqlite3.connect("pvSmartHome.db",check_same_thread=False)
        self.c = self.conn.cursor()

        self.c.execute('CREATE TABLE IF NOT EXISTS "pvStats" ("id"	INTEGER, "output"	REAL NOT NULL, "usage"	REAL NOT NULL, "gridPower"	REAL NOT NULL, "timestamp"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY("id" AUTOINCREMENT));')
        self.c.execute('CREATE TABLE IF NOT EXISTS "powerThresholds" ("ain"	TEXT NOT NULL UNIQUE,"name" TEXT,"threshold"	REAL, "priority" INTEGER DEFAULT 0, "automationState" INTEGER, "powerState" INTEGER, PRIMARY KEY("ain"));')
        self.c.execute('CREATE TABLE IF NOT EXISTS "powerStateChange" ("id"	INTEGER, "ain"	TEXT NOT NULL,"stateChange"	TEXT, "timestamp"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY("id" AUTOINCREMENT));')
        self.c.execute('CREATE TABLE IF NOT EXISTS "accounts" ("tool"	TEXT,"username"	TEXT,"password"	TEXT);')
        self.c.execute('CREATE TABLE IF NOT EXISTS "settings" ("automation"	INTEGER NOT NULL DEFAULT 0 , "updateTime" INTEGER NOT NULL DEFAULT 0);')

        sql = 'SELECT COUNT(*) FROM accounts WHERE tool = "FritzBox"'
        self.c.execute(sql)
        if(self.c.fetchone()[0] != 1):
            self.resetPassword("FritzBox")

        sql = 'SELECT COUNT(*) FROM accounts WHERE tool = "webSolar"'
        self.c.execute(sql)
        if(self.c.fetchone()[0] != 1):
            self.resetPassword("webSolar")

        sql = "SELECT COUNT(*) FROM settings"
        self.c.execute(sql)
        if(self.c.fetchone()[0] != 1):
            self.c.execute("INSERT INTO settings VALUES (0,0)")
            self.conn.commit()
       
    def updateSavedDevices(self, deviceList: dict):
         

        savedDevices = self.c.execute("SELECT ain FROM powerThresholds").fetchall()

        savedDevicesList = []
        for device in savedDevices:
            savedDevicesList.append(device[0])

        for device in deviceList:
            if device not in savedDevicesList:
                self.c.execute("INSERT INTO powerThresholds VALUES (?,?,0,0,0,0)",(device,deviceList.get(device) ))
                self.conn.commit()
 

    def getAccount(self,tool: str):
         
        self.c.execute('SELECT username, password FROM accounts WHERE tool=?',(tool,))
        return self.c.fetchone()

    def setAccount(self, tool: str, username: str, pw: str):
         
         
        self.c.execute('DELETE FROM accounts WHERE tool = ?',(tool,))
        self.c.execute('INSERT INTO accounts VALUES (?,?,?)', (tool, username, pw))
        self.conn.commit()

    def getSavedDeviceInformation(self):
         

        self.c.execute("SELECT * FROM powerThresholds ORDER BY priority DESC")

        return self.c.fetchall()


    def getThreshold(self, ain: str):
         

        self.c.execute('SELECT threshold FROM powerThresholds WHERE ain = ?',(ain,))

        return self.c.fetchone()[0]

       

    def setThreshold(self, ain: str, threshold: float):

        self.c.execute("UPDATE powerThresholds SET threshold=? WHERE ain=?",(threshold,ain))
        self.conn.commit()

    def getPriority(self, ain: str):
        

        self.c.execute('SELECT priority FROM powerThresholds WHERE ain = ?',(ain,))

        return self.c.fetchone()[0]

       

    def setPriority(self, ain: str, priority: int):
          
        self.c.execute("UPDATE powerThresholds SET priority=? WHERE ain=?",(priority,ain))
        self.conn.commit()

    def getAutomationState(self, ain:str):
         

        self.c.execute("SELECT automationState FROM powerThresholds WHERE ain=?",(ain,))
        return (self.c.fetchone()[0] == 1)

    def activateDevice(self, ain:str):
         

        self.c.execute("UPDATE powerThresholds SET automationState=1 WHERE ain=?",(ain,))
        self.conn.commit()
     
    def deactivateDevice(self, ain:str):
         

        self.c.execute("UPDATE powerThresholds SET automationState=0 WHERE ain=?",(ain,))
        self.conn.commit()

    def addPvOutput(self,output: float):
         

        self.c.execute("INSERT INTO pvOutput (output) VALUES (?) ",(output,))
        self.conn.commit()

    def addPvData(self, output: float, usage: float, gridPower: float):
         
        print("outout: " + str(output) + "  usage: " + str(usage) + "  gridPower: " + str(gridPower))
        self.c.execute("INSERT INTO pvStats (output, usage, gridPower) VALUES (?,?,?) ",(output,usage, gridPower))
        self.conn.commit()


    def trackStateChange(self, ain: str, stateChangeType: str):
         

        self.c.execute('INSERT INTO powerStateChange (ain, stateChange) VALUES (?,?)',(ain, stateChangeType))
        self.conn.commit()

    
    def resetPassword(self, tool:str):
        self.c.execute('DELETE FROM accounts WHERE tool = ?',(tool,))
        username = input("Enter " + tool + " Username: ")
        password = input("Enter " + tool + " Password: ")
        self.c.execute("INSERT INTO accounts VALUES (?,?,?)",(tool,username,password))
        self.conn.commit()
        print("Account for " + tool + " updated")

    def getUpdateTime(self):
         

        self.c.execute('SELECT updateTime FROM settings')
        
        return self.c.fetchone()[0]

       

    def setUpdateTime(self, updateTime: int):
          
         

        
        self.c.execute("UPDATE settings SET updateTime=?",(updateTime,))
        self.conn.commit()
        
    
    def getAutomation(self):
         

        self.c.execute('SELECT automation FROM settings')

        return self.c.fetchone()[0]

       

    def setAutomation(self, automation: int):
          
           
        self.c.execute("UPDATE settings SET automation=?",(automation,))
        self.conn.commit()

    
    def getLastDataInput(self):

        self.c.execute("SELECT COUNT(*) FROM pvStats")
        
        if(self.c.fetchone()[0] != 0):
            self.c.execute("SELECT * FROM pvStats ORDER BY id DESC LIMIT 1 ")
            return self.c.fetchone()
        else:
            #database is empty, return first date
            return [0,0,0,0,"1970-01-01 00:00:00"]

    def getPvData(self):

        self.c.execute("SELECT * FROM pvStats")

        return self.c.fetchall()

    def getPvDataLimit(self, limit: int):

        self.c.execute("SELECT * FROM pvStats ORDER BY id DESC LIMIT ? ",(limit,))

        return self.c.fetchall()

    def getPvDataCurrentDay(self):
        timestamp = datetime.combine(datetime.now(), time.min)

        self.c.execute("SELECT * FROM pvStats WHERE timestamp > ? ORDER BY id DESC",(timestamp,))

        return self.c.fetchall()

    def updatePowerState(self, ain:str, powerState):
        value = 0
        if(powerState):
            value = 1

        self.c.execute("UPDATE powerThresholds SET powerState = ? WHERE ain = ?",(value,ain))
        self.conn.commit()


    def closeConnection(self):
         
         
        self.c.close()
        self.conn.close()
        
        