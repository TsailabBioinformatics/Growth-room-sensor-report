import json
import sqlite3
import pandas as pd

def readJson(filename):
    try:
        data = open(filename,"r")
        data = json.loads(data.read())
        return data
    except Exception as e:
        print("Error: ", e)
        return ""

def writeJson(path, newdata):
    try:
        with open(path,"w") as config:
            json.dump(newdata,config)
        return 1
    except :
        return 0
        
def readSqlite(query):
    conn = sqlite3.connect("RPI-Data.db")
    df = pd.read_sql_query(query, conn)
    return df


def saveSqlite(query):
    conn = sqlite3.connect("RPI-Data.db")
    try:
        conn.execute(query)
        conn.commit()
        conn.close()
        return 1
    except:
        return 0 