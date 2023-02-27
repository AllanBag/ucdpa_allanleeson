####https://data.smartdublin.ie/mobybikes-api
###likely will just use to call current data to compare to historical

import requests

request = requests.get('https://data.smartdublin.ie/mobybikes-api/last_reading')

print(request.json())