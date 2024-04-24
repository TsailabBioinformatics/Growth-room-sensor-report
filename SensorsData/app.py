from flask import Flask, jsonify,request
from flask_cors import CORS
from userdefined import *
from datetime import datetime
import json



'''  initialize app for flask '''
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}},support_credentials=True)
    
    
'''  renders home page of the application '''
@app.route('/database',methods=['GET'])
def default():
    return "connected"



@app.route('/database/storedata',methods=['POST'])
def getdata():
    data = request.get_json()
    
        
    data = json.loads(data)
    now = datetime.now()
    dt = now.strftime("%d-%m-%Y %H:%M:%S")
    data["timestamp"] = dt
    print("---data--",data["timestamp"])
    print("---data--",data["IPAddress"])
    print("rpi", data["rpi"])
    if data["rpi"] == "blackbox_bmp180":
        query = "INSERT INTO {} VALUES( {}, '{}', '{}', {}, '{}','{}','{}')".format(data["rpi"], data["Pressure"],data["IPAddress"],data["ImgRef"],data["Temperature"], timeStamp,0,data["image"],data["location"])
    elif data["rpi"] in ("sonya_cummings","lilli_speight"):
        query = "INSERT INTO {} VALUES( {}, '{}', '{}', {}, {},'{}',{},'{}','{}',{})".format(data["rpi"], data["Humidity"],data["IPAddress"],data["ImgRef"],data["Motion"],data["Temperature"], data["timestamp"],0,data["image"],data["location"],data["brightness"])
    else:
        query = "INSERT INTO {} VALUES( {}, '{}', '{}', {}, {}, '{}', '{}',{},'{}','{}',{})".format(data["rpi"], data["Humidity"],data["IPAddress"],data["ImgRef"],data["Motion"],data["Temperature"],data["Thermal"], data["timestamp"],0,data["image"],data["location"],data["brightness"])
        
    status = saveSqlite(query)
    print(status)
    print(datetime.now())
    
    
    return "true"
    
    
'''  The service runs on port 8071 '''
if __name__ == '__main__':
    app.run(host='172.30.18.104', port=8071, debug=True)