import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import psycopg2
import string

TypeOfdays = ["Monday_start","Monday_end", "Tuesday_start", "Tuesday_end", "Wednesday_start", "Wednesday_end", "Thursday_start", "Thursday_end","Friday_start","Friday_end","Saturday_start", "Saturday_end","Sunday_start","Sunday_end"]
url = "https://cafenomad.tw/shop/"

def MasterScrape(cafeID):
    hasPourOverCafe = False
    index = 0
    st = ""
    finalUrl = url + cafeID

    resp = requests.get(finalUrl).text #getting the info for the specific cafe
    soup1 = BeautifulSoup(resp, "html.parser")
    datetags = soup1.find_all('div', class_="time")
    foodtags = soup1.find_all('div', class_="rating-box")
    images = soup1.find_all('img')
    if soup1.get_text().find("手沖") >= 0:
        hasPourOverCafe = True
    temp = {"ID": cafeID, "pour_over": hasPourOverCafe,"photos": []}
    if not(resp.__contains__("目前還沒有人提供這間店的照片")):
        for im in images:
            tempstring = str(im['src'])
            if tempstring.__contains__("/upload_photos"):
                tempstring = "https://cafenomad.tw/" + tempstring
                temp['photos'].append(tempstring)
            elif tempstring.__contains__("/img/cta/"):
                continue
    if len(datetags) == 0:
        for days in TypeOfdays:
            temp[days] = ""
    else:
        for d in datetags:
            t = d.text.translate({ord(c): None for c in string.whitespace})
            if t == "未營業":
                temp[TypeOfdays[index]] = "Not Open"
                index+=1
                temp[TypeOfdays[index]] = "Not Open"
                index+=1
            else:
                for letter in t:
                    if letter == "-":
                        temp[TypeOfdays[index]] = st
                        index += 1
                        st = ""
                    else:
                        st = st + letter
                temp[TypeOfdays[index]] = st
                index += 1
                st = ""
    for a in foodtags:
        p = a.text.translate({ord(c): None for c in string.whitespace})
        if p == "有賣單品Yes":
            temp["single_origin"] = True
        elif p == "有賣單品No":
            temp["single_origin"] = False
        elif p == "有賣單品":
            temp["single_origin"] = "No-Info"
        if p == "有賣甜點Yes":
            temp["desserts"] = True
        elif p == "有賣甜點No":
            temp["desserts"] = False
        elif p == "有賣甜點":
            temp["desserts"] = "No-Info"
        if p == "有賣正餐Yes":
            temp["meals"] = True
        elif p == "有賣正餐No":
            temp["meals"] = False
        elif p == "有賣正餐":
            temp["meals"] = "No-Info"
    return temp

if __name__ == "__main__":
    updatedCafeInfo = []
    with open('cafes_id.json', 'r') as cafes_file:
        cafeList = json.load(cafes_file)
    for cafe in cafeList:
        updatedCafeInfo.append(MasterScrape(cafe['id']))
        #returns the updated cafe information
    with open('updated_cafeData.json','w') as CafeDataUpdate:
        json.dump(updatedCafeInfo,CafeDataUpdate)
        #print(result)