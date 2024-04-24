'''
    Import necessary packages
'''
import os
import json
from sendEmail import *
from datetime import datetime
import logging
from userdefined import *

configdata = readJson("/home/sonya-cummings/trackIPadress/config.json")


rpidescription = "sonya_cummings"

def storeOnWebserver(data,url):
    data_str = json.dumps(data)
    # Send the JSON string to the API endpoint
    response = requests.post(url, json=data_str)

    return json.loads(response.text)


'''    
    get location of the RPI from firebase  
'''
details = storeOnWebserver({"rpidescription": rpidescription},'http://aspendb.uga.edu/rpi0/emailgetdata')
location,currentIP = details["location"], details["currentIP"]


        
'''
    Get IP address of the Raspberry Pi
'''
def raspberryIP():
    ip = ""
    routes = json.loads(os.popen("ip -j -4 route").read())
    for r in routes:
        if r.get("dev") == "wlan0" and r.get("prefsrc"):
            ip = r["prefsrc"]
        break
    return ip


'''
    Logger to record error
'''
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.warning(f"The [{rpidescription}-pi3-{location}] getIP.py start")


'''
    Making call to raspberryIP() and sending an email to indicate that the raspberryPi was started/restarted
'''
newIP = raspberryIP()
sendStaus(currentIP, newIP, "the script/service was restarted", 0, location,rpidescription)


'''
    Infinite loop to keep this app running and Making call to raspberryIP() and sending an email if there is a change in IP address
'''
while True:
    newIP = raspberryIP()
    if currentIP!= newIP:
        sendStaus(currentIP, newIP, "the IP have been changed",1, location,rpidescription)
        currentIP = newIP
        configdata["IP"]=newIP
        value = writeJson(configdata)
        
        ''' save the updated data into the firebase '''
        field_updates = {"IPAddress": newIP, "rpidescription":rpidescription}
        details = storeOnWebserver(field_updates,'http://aspendb.uga.edu/rpi0/emailsavedata')

        logging.warning(f"The [{rpidescription}-pi3-{location}] IP changed and write file status: {value}")
        

