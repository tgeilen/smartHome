
from FritzHomeAuto import FritzHomeAuto
from Settings import Settings


class FHAHandler:

    global fha
    
    def __init__(self, user: str, password: str):
        print("Setting up FritzHome Handler")
        try:
            global fha


            host = 'http://fritz.box'
            

            fha = FritzHomeAuto(user,password,host)

            #fha = FritzHomeAuto(user, pw, host)
            print("successfully set up FritzHome Handler")
        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Connecting to FritzBox failed")
            print("Make sure the VPN is activated")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    def getDevices(self):
        global fha
        return fha.get_switch_list()

    def getOutput(self, ain: str):
        global fha
        output = fha.get_state(ain).get("power")

        if(type(output) == str):
            return output
        
        else:
            return "error"

    def getState(self, ain:str):
        global fha
        return fha.get_state(ain).get("state")

    def changeState(self, ain:str, newState: str):
        global fha
        return fha.switch(ain, newState)

       
    def getFHA(self):
        global fha
        return fha