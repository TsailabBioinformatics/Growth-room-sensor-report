import os
import json
from sendEmail import *
from datetime import datetime
import logging
from userdefined import *
import firebase_admin
from firebase_admin import credentials, firestore, storage

configdata = readJson("/home/wendy-king/trackIPadress/config.json")


'''  firebase db-key  '''
cred = credentials.Certificate("/home/wendy-king/trackIPadress/db-key.json")

'''  initialize_app for firebase database '''
firebase_admin.initialize_app(cred)
db = firestore.client()

rpidescription = "wendy-king"


'''    get location of the RPI from firebase  '''
try:
    doc_ref = db.collection("RPI-details")
    for doc in doc_ref.get():
        if doc.id == rpidescription:
            location = doc.to_dict()["location"]
            currentIP = doc.to_dict()["IPAddress"]
            break
except:
    location = ""
    currentIP = ""

        
    
def raspberryIP():
    ip = ""
    routes = json.loads(os.popen("ip -j -4 route").read())
    for r in routes:
        if r.get("dev") == "wlan0" and r.get("prefsrc"):
            ip = r["prefsrc"]
        break
    return ip



logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.warning(f"The [{rpidescription}-pi3-{location}] getIP.py start")



newIP = raspberryIP()
sendStaus(currentIP, newIP, "the script/service was restarted", 0, location,rpidescription)

while True:
    newIP = raspberryIP()
    if currentIP!= newIP:
        sendStaus(currentIP, newIP, "the IP have been changed",1, location,rpidescription)
        currentIP = newIP
        configdata["IP"]=newIP
        value = writeJson(configdata)
        
        ''' save the updated data into the firebase '''
        field_updates = {"IPAddress": newIP}
        try:
            doc_ref = db.collection("RPI-details")
            for doc in doc_ref.get():
                if doc.id == rpidescription:
                    doc_ = db.collection("RPI-details").document(doc.id)
                    doc_.update(field_updates)
                    break
        except:
            continue 

        logging.warning(f"The [{rpidescription}-pi3-{location}] IP changed and write file status: {value}")
        

