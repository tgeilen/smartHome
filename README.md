## Solenuo - Solar Energy Usage Optimiser
This tool allows to automatically power on and off AVM SmartHome Switches depending on the power output of solar panels.

Via a web app the automation can be activated or deactivated and thresholds can be set for all connected smarthome devices.
Additionally, an analytics dashboard provides insight in the power usage and production of the system and displays historic data.

The production data of the solar panels as well as the total power usage of the household are scraped from the Fronius WebSolar website in real time using Selenium and stored in a database.

This tool is built to run a computer (e.g. as Raspberry Pi) within the network or with a VPN connection to the FritzBox.

Run the following code in your terminal to install and start the tool:

```
git clone https://github.com/tgeilen/solenuo.git
cd smartHome 
python3 -m venv venv 
pip3 install -r requirements.txt 
export FLASK_APP=webserver.py 
flask run --host=0.0.0.0
python3 FritzSmartHome.py
```

<a href="https://imgur.com/Kj7ISSG"><img src="https://i.imgur.com/Kj7ISSG.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/Ij5dLTN"><img src="https://i.imgur.com/Ij5dLTN.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/t5yJuyD"><img src="https://i.imgur.com/t5yJuyD.png" title="source: imgur.com" /></a>
