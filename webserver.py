from concurrent.futures import thread
from crypt import methods
from DBHandler import DBHandler
from flask import Flask, request, redirect, url_for, render_template, Request
from automationThread import automationThread
from datetime import datetime
 


app = Flask(__name__)



@app.route('/')
def index():
    global updateTime
    db = DBHandler()
    deviceInformation = db.getSavedDeviceInformation()

    
    lastUpdate = datetime.strptime(db.getLastDataInput()[4],"%Y-%m-%d %H:%M:%S")
    warningActive = False
    print(lastUpdate)
    duration = datetime.utcnow() - lastUpdate
    durationInSec = duration.total_seconds()
    if(durationInSec > 60):
        print("im in the if")
        warningActive = True

    automationRunning = db.getAutomation()==1
    updateTime = db.getUpdateTime()
    timeUnit = ""
    if (updateTime % (3600) == 0):
        updateTime = round(float(updateTime) / 3600) 
        timeUnit = "h"
    elif (updateTime % (60) == 0):
        updateTime = round(float(updateTime) / 60) 
        timeUnit = "min"
    else:
        timeUnit = "sec"

    
    return render_template("index.html", deviceInformation= deviceInformation, automationRunning = automationRunning, updateTime = updateTime, timeUnit=timeUnit, warningActive=warningActive)


@app.route('/statistics')
def dashbaord():
    db = DBHandler()

    data = db.getPvDataCurrentDay()
    ids = []
    output = []
    usage = []
    gridInput = []
    for entry in reversed(data):
        ids.append(entry[0])
        output.append(entry[1])
        usage.append(entry[2])
        gridInput.append(entry[3])

    return render_template("statistics.html", data=data, ids=ids, output=output, usage = usage, gridInput=gridInput)

@app.route("/updateAutomation", methods=["POST"])
def updateAutomation():
    db = DBHandler()
    print(request.form)
    updateTime = request.form.get("updateTime")
    print(updateTime)
    print("updatetime")
    timeUnit = request.form.get("timeUnit")
    print(timeUnit)
    print("timeUnit")
    multiplier = 0
    if(timeUnit == "h"):
        multiplier == 3600
    elif(timeUnit == "min"):
        multiplier = 60
    else:
        multiplier = 1

    db.setUpdateTime(str(round(float(updateTime))*multiplier))
   
    #db.setAutomation(1 if request.form.get("automationState") else 0)
    if(request.form.get("automationState") == 'true'):
        print("hello its working")
        db.setAutomation(1)
    else:
        print("hello its not asdads working")
        db.setAutomation(0)
    
    return "<head> <meta http-equiv='refresh' content='0; URL=/'></head>"


@app.route("/settings", methods=["POST"])
def settings():
    db = DBHandler()
    ain = request.form.get("ain")
    name = request.form.get("name")
    automationState = db.getAutomationState(ain)
    threshold = db.getThreshold(ain)
    priority  = db.getPriority(ain)
    return render_template("settings.html",ain=ain,name=name,automationState=automationState,threshold=threshold, priority=priority)

@app.route("/updateInformation", methods=["POST"])
def updateInformation():
    db = DBHandler()
    ain = request.form.get("ain")
    threshold = request.form.get("thresholdInput")
    automationState = request.form.get("automationState")
    priority = request.form.get("priority")

    if(threshold != ''):
        db.setThreshold(ain, float(threshold))

    if(automationState == "true"):
        db.activateDevice(ain)
    else:
        db.deactivateDevice(ain)

    db.setPriority(ain, priority)


    return "<head> <meta http-equiv='refresh' content='0; URL=/'></head>"

if __name__ == '__main__':
   app.run(debug=True, port=80, host='0.0.0.0')