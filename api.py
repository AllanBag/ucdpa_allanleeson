####https://data.smartdublin.ie/mobybikes-api
###likely will just use to call current data to compare to historical

import requests
import pandas as pd
import json

###grabs a snapshot of the current state of things and returns an object
request = requests.get('https://data.smartdublin.ie/mobybikes-api/last_reading')
snapshot = request.json()
snapshot = pd.read_json(json.dumps(snapshot))

#print(snapshot)