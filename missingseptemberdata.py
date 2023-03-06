####https://data.smartdublin.ie/mobybikes-api
###Using this script to replace missing September data not provided on the moby bikes dataset listed below, data can still be accessed via the API.

#####https://data.smartdublin.ie/mobybikes-api
###moby-bikes-historical-data-092022.csv


import requests
import pandas as pd
import json
from pandas import json_normalize

import requests
import json
import csv

r = requests.get('https://data.smartdublin.ie/mobybikes-api/historical', params={'start':'2022-09-01', 'end':'2022-09-30'})
data= r.text
###converting to something json_normalize can interpret
data= json.loads(data)
df= json_normalize(data)
print(df)


df.to_csv (r'C:\Users\Allan\PycharmProjects\mobyproject\2022\moby-bikes-historical-data-092022.csv', index = None, header=True)
