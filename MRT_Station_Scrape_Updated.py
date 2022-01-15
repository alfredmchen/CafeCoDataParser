import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import psycopg2
import string

MRT_TYPES = ["TRTC","KRTC","KLRT","TYMC","NTDLRT","TRTCMG"]
url = "https://ptx.transportdata.tw/MOTC/v2/Rail/Metro/Station/"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,image/webp,*/*;q=0.8'
    }

def MRT_update(url, headers, MRT_TYPES):
    listOfMRT = []
    for types in MRT_TYPES:
        finalUrl = url + types + "?$format=JSON"
        resp = requests.get(finalUrl,headers=headers).text
        MRT_station_info = json.loads(resp)
        temp = {}
        for stations in MRT_station_info:
            temp["StationUID"] = stations["StationUID"]
            temp["StationID"] = stations["StationID"]
            temp["StationName"] = stations["StationName"]["Zh_tw"]
            if stations.get("StationAddress") is None:
                temp["StationAddress"] = ""
            else:
                temp["StationAddress"] = stations["StationAddress"]
            temp["Latitude"] = stations["StationPosition"]["PositionLat"]
            temp["Longtitude"] = stations["StationPosition"]["PositionLon"]
            temp["LocationCity"] = stations["LocationCity"]
            # print(temp)
            listOfMRT.append(temp)
    # print(listOfMRT)
    with open('MRT_INFO.json', 'w') as MRT_ID_file:
        json.dump(listOfMRT, MRT_ID_file)

if __name__ == '__main__':
    MRT_update(url, headers, MRT_TYPES)