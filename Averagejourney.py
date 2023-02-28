import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import os
import glob
import re

path = 'C:\\Users\\Allan\PycharmProjects\mobyproject\\2020'
csv_files = glob.glob(os.path.join(path, "*.csv"))

###pull year from alldata
def get_year(date):
    return re.search(r"\d{4}", date).group(0)

# loop over the list of csv files to give us a full year dataset
alldata = pd.DataFrame()

for f in csv_files:
    # read the csv file
    df = pd.read_csv(f, usecols=['HarvestTime','BikeID','Latitude','Longitude'])
    # append the content
    alldata =  pd.concat([alldata, df])

alldata['Year'] = get_year(str(alldata['HarvestTime']))
alldata.sort_values(by = 'HarvestTime')

###print a whole year of data
print(alldata)



def bikeselect(bikeno, dataset):
    ######to find a given bikes journeys, and remove periods where the bike was stationary
    bikedata = dataset.loc[dataset['BikeID'] == bikeno]
    bikedata = bikedata.drop_duplicates(['Latitude', 'Longitude'], keep='last')
    ###bikedata= pd.concat([bikedata1, bikedata2])
    return(bikedata)

def journeys(bikeno, dataset):
    ###returns distance travelled for a given bike in a dataset
    locationdata = bikeselect(bikeno, dataset)

    latchange =    locationdata['Latitude'].diff()
    longchange =    locationdata['Longitude'].diff()

    ###conversion rates
    ###Latitude: 1deg = 110.574 km
    ###Longitude: 1 deg = 111.320 * cos(latitude) km
    ###take a constant for longitude instead of trying to vary based on latitude
    longchange = longchange * 111320* np.cos(0.925025)
    latchange = latchange * 110574

    ###return the changes in lat and longitude and find the distance between the two points
    diff = (pd.merge(latchange, longchange, right_index = True,
               left_index = True)).dropna()
    diff['distance'] = [np.sqrt(x**2 + y**2) for x, y in zip(diff['Latitude'], diff['Longitude'])]

    #omit short hops where bike could have been moved by external factors as bikes do not have a hardpoint docking station
    ###ie they can be dragged, locked to movable objects etc

    diff.drop(diff[diff['distance'] <= 100].index, inplace=True)
    return diff['distance']

alljourneysinyear = [journeys(bike, alldata) for bike in zip(alldata['BikeID'])]


print(alljourneysinyear)