####https://data.smartdublin.ie/mobybikes-api
###Using this script to replace missing September data not provided on the moby bikes dataset listed below
#####https://data.smartdublin.ie/mobybikes-api
import requests
import pandas as pd
import json

###grabs a snapshot of the current state of things and returns an object
request = requests.get('https://data.smartdublin.ie/mobybikes-api/historical', params={'start':'2022-09-01', 'end':'2022-09-30'})
snapshot = request.json()
snapshot = pd.read_json(json.dumps(snapshot))

print(snapshot)