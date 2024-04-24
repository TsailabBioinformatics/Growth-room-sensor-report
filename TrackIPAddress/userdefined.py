import json


def readJson(filename):
    try:
        data = open(filename,"r")
        data = json.loads(data.read())
        return data
    except Exception as e:
        print("Error: ", e)
        return ""

def writeJson(newdata):
    try:
        with open("/home/wendy-king/trackIPadress/config.json","w") as config:
            json.dump(newdata,config)
        return 1
    except :
        return 0