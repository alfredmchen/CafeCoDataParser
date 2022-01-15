import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import psycopg2

url = "https://cafenomad.tw/api/v1.2/cafes"

def getInfo(url):
    resp = requests.get(url).text
    soup1 = BeautifulSoup(resp, "html.parser")
    site_json = json.loads(soup1.text)
    table = pd.DataFrame(columns=("Name", "City", "Address", "Socket", "Wifi"))
    temp = {}
    for item in site_json:
        temp["Name"] = item["name"]
        # temp["City"] = item["city"]
        # temp["Address"] = item["address"]
        # temp["Socket"] = item["socket"]
        # temp["Wifi"] = item["wifi"]
        # temp["OpenTime"] = item["open_time"]
        table = table.append(temp, ignore_index=True)
    return table

if __name__ == '__main__':
    # conn = psycopg2.connect(user="uiakbrlliktsow",
    #                         password="2eb7e36688c4593979ea7f36bbd7a729363925983105c969e3c6e26e060329db",
    #                         host="ec2-52-7-39-178.compute-1.amazonaws.com",
    #                         port=5432,
    #                         database="d6l2o9f2eu7nf5")
    # print("PostgreSQL server information")
    # print(conn.get_dsn_parameters(), "\n")
    finaltable = getInfo(url)
