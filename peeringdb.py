import urllib.request
import json
import os
import pandas as pd

BASEURL = 'https://publicdata.caida.org/datasets/peeringdb/{year:04d}/{month:02d}/peeringdb_2_dump_{year:02d}_{month:02d}_{day:02d}.json'
DIRNAME = './data/'

def _download(url, filename):
    with urllib.request.urlopen(url) as f:
        json_data = json.loads(f.read())
    
    with open(filename, 'w') as g:
        json.dump(json_data, g)

    return json_data

def load(year, month, day):
    url = BASEURL.format(year=year, month=month, day=day)
    os.makedirs(DIRNAME, exist_ok=True)
    filename = DIRNAME + url.split('/')[-1]

    if os.path.isfile(filename):
        with open(filename) as f:
            json_data = json.load(f)
    else:
        json_data = _download(url, filename)

    return json_data

def create_dataframes(json_data):
    dic = {}
    for key in json_data.keys():
        df = pd.DataFrame(json_data[key]['data'])
        dic[key] = df
    return dic
