## Fritz SmartHome Automation

This tool allows to automatically power on and off AVM SmartHome Switches depending on the power output of solar panels.

Via a web app the automation can be activated or deactivated and thresholds can be set for all connected smarthome devices.
Additionally, an analytics dashboard provides insight in the power usage and production of the system and displays historic data.

The production data of the solar panels as well as the total power usage of the household are scraped from the Fronius WebSolar website in real time using Selenium and stored in a database.

This tool is built to run a computer (e.g. as Raspberry Pi) within the network or with a VPN connection to the FritzBox.


