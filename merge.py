import pandas as pd

import matplotlib.pyplot as plt

import numpy as np

import seaborn as sns



ca = pd.read_csv(r"D:\Datasets\Moby Bikes Historical Data\moby-bikes-historical-data-032021.csv")

print(np.median(ca['SpikeID']))


#####df = df[df.line_race != 0]

cb = pd.read_csv(r"D:\Datasets\Moby Bikes Historical Data\moby-bikes-historical-data-042021.csv")

frames = [ca,cb]

combine = pd.concat(frames)
combine=combine[combine.Longitude !=0]

x, y = combine['Latitude'],combine['Longitude']
print(combine.head(5))


bike36 = combine.loc[combine['BikeID'] == 36]

print(bike36.head(10))

def bikeselect(bikeno, dataset):
    ######to find a given bikes journeys, and remove periods where the bike was stationary
    bikedata = dataset.loc[dataset['BikeID'] == bikeno]

    bikedata = bikedata.drop_duplicates(['Latitude', 'Longitude'], keep='last')
    ###bikedata= pd.concat([bikedata1, bikedata2])

    return(bikedata)


def journeys(bikeno, dataset):
    ###returns distance travelled and a very rough travel time
    locationdata = bikeselect(bikeno, dataset)

    latchange =    locationdata['Latitude'].diff()
    longchange =    locationdata['Longitude'].diff()

    ###conversion rates
    ###Latitude: 1deg = 110.574 km
    ###Longitude: 1 deg = 111.320 * cos(latitude) km

    longchange = longchange * 111320* np.cos(0.925025)
    latchange = latchange * 110574

    ###return the changes in lat and longitude and find the distance between the two points
    diff = (pd.merge(latchange, longchange, right_index = True,
               left_index = True)).dropna()
    diff['distance'] = [np.sqrt(x**2 + y**2) for x, y in zip(diff['Latitude'], diff['Longitude'])]


    diff.drop(diff[diff['distance'] <= 200].index, inplace=True)

    return diff['distance'], locationdata['HarvestTime']

tester = journeys(36, combine)

tester = pd.DataFrame(tester)


print(tester.head())
