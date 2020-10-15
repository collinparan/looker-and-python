#!usr/bin/python

import requests
import json
import pandas as pd

looker_instance = "<your instance>"
client_id = "<client id>"
client_secret = "<client secret>"
look = "<look number you want to pull data from>"


def looker_auth_token():
    url = "https://"+looker_instance+".looker.com:19999/api/3.0/login"
    querystring = {"client_id": client_id, "client_secret": client_secret}
    headers = {
        'cache-control': "no-cache"
        }
    response = requests.request("POST", url, headers=headers, params=querystring)
    res = json.loads(response.text)
    return res["access_token"]


def get_look_data(look_num):
    url = "https://"+looker_instance+".looker.com:19999/api/3.0/looks/"+look_num+"/run/json"
    querystring = {"apply_formatting": "false", "apply_vis": "false", "generate_drill_links": "false"}
    headers = {
        'Authorization': "Bearer " + looker_auth_token(),
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)
    return res


data = get_look_data(look)

#Converts json data to dataframe
df = pd.DataFrame.from_dict(data, orient='columns')

#Descriptive statistics
print(df.head(5))
print(df.describe())
