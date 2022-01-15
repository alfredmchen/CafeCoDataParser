import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import psycopg2
import string

TypeOfdays = ["Monday-open","Monday-close", "Tuesday-open", "Tuesday-close", "Wednesday-open", "Wednesday-close","Thursday-open", "Thursday-close","Friday-open","Friday-close","Saturday-open", "Saturday-close","Sunday-open","Sunday-close"]
url = "https://cafenomad.tw/shop/"

def updatePourOverCafes(url):
    hasPourOverCafe = False
    listofCafes =[]
    index = 0
    str = ""
    with open('cafes_id.json', 'r') as cafes_file:  # loads the JSON file with only cafe id s
        cafes = json.load(cafes_file)
    for ca in cafes:
        finalUrl = url + ca['id']
        resp = requests.get(finalUrl).text #getting the info for the specific cafe
        soup1 = BeautifulSoup(resp, "html.parser")
        datetags = soup1.find_all('div', class_="time")
        foodtags = soup1.find_all('div', class_="rating-box")
        if soup1.get_text().find("手沖") >= 0:
            hasPourOverCafe = True
        temp = {"id": ca['id'], "hasPourOver": hasPourOverCafe}
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
                            temp[TypeOfdays[index]] = str
                            index += 1
                            str = ""
                        else:
                            str = str + letter
                    temp[TypeOfdays[index]] = str
                    index += 1
                    str = ""
        for a in foodtags:
            p = a.text.translate({ord(c): None for c in string.whitespace})
            if p == "有賣單品Yes":
                temp["has單品"] = True
            elif p == "有賣單品No":
                temp["has單品"] = False
            elif p == "有賣單品":
                temp["has單品"] = "No-Info"
            if p == "有賣甜點Yes":
                temp["has甜點"] = True
            elif p == "有賣甜點No":
                temp["has甜點"] = False
            elif p == "有賣甜點":
                temp["has甜點"] = "No-Info"
            if p == "有賣正餐Yes":
                temp["has正餐"] = True
            elif p == "有賣正餐No":
                temp["has正餐"] = False
            elif p == "有賣正餐":
                temp["has正餐"] = "No-Info"
        index = 0
        print(temp)
        listofCafes.append(temp)
        hasPourOverCafe = False #reset

if __name__ == '__main__':
    updatePourOverCafes(url)
