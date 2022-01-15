import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import psycopg2

url = "https://cafenomad.tw/shop/"

def test(url):
    cafeInfo = []
    tempInfo = {"ID":"","Images":[]}
    tempInfo["ID"] = "73e0ddbf-4762-42ec-89aa-c278765d0e3c"
    resp = requests.get(url).text  # getting the info for the specific cafe
    soup1 = BeautifulSoup(resp, "html.parser")
    images = soup1.find_all('img')
    num = 0
    if resp.__contains__("目前還沒有人提供這間店的照片"):
        print("d")
    for im in images:
        temp = str(im['src'])
        print(temp)
        if temp.__contains__("/upload_photos"):
            temp = "https://cafenomad.tw/" + temp
            tempInfo['Images'].append(temp)
            num+=1
        elif temp.__contains__("/img/cta/"):
            temp = ""
    cafeInfo.append(tempInfo)
    print(cafeInfo)
    print(num)


def scrapeImages(url):
    cafeInfo = []
    with open('cafes_id.json', 'r') as cafes_file:  # loads the JSON file with only cafe id s
        cafeList = json.load(cafes_file)
    for cafe in cafeList:
        finalUrl = url + cafe['id']
        resp = requests.get(finalUrl).text  # getting the info for the specific cafe
        soup1 = BeautifulSoup(resp, "html.parser")
        images = soup1.find_all('img')
        if resp.__contains__("目前還沒有人提供這間店的照片"):
            tempInfo = {"ID": "", "Images": []}
            tempInfo['ID'] = cafe['id']
            tempInfo['Images'] = []
            print(tempInfo)
            cafeInfo.append(tempInfo)
        else:
            tempInfo = {"ID": "", "Images": []}
            tempInfo['ID'] = cafe['id']
            for im in images:
                temp = str(im['src'])
                if temp.__contains__("/upload_photos"):
                    temp = "https://cafenomad.tw/" + temp
                    tempInfo['Images'].append(temp)
                elif temp.__contains__("/img/cta/"):
                    continue
            print(tempInfo)
            cafeInfo.append(tempInfo)
    with open('cafes_id_Image_update.json', 'w') as cafes_id_file:
        json.dump(cafeInfo, cafes_id_file)

    print(cafeInfo)

if __name__ == '__main__':
    scrapeImages(url)
    #test(url)

