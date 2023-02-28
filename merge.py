import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import glob
import os

###comments

path = 'C:\\Users\\Allan\PycharmProjects\mobyproject\\2022'
csv_files = glob.glob(os.path.join(path, "*.csv"))

# loop over the list of csv files
alldata = pd.DataFrame()

for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)
    # append the content
    alldata = pd.concat([alldata, df])


def bikeselect(bikeno, dataset):
    ######to find a given bikes journeys, and remove periods where the bike was stationary
    bikedata = dataset.loc[dataset['BikeID'] == bikeno]

    bikedata = bikedata.drop_duplicates(['Latitude', 'Longitude'], keep='last')
    ###bikedata= pd.concat([bikedata1, bikedata2])

    return (bikedata)


def journeys(bikeno, dataset):
    ###returns distance travelled and a very rough travel time
    locationdata = bikeselect(bikeno, dataset)

    latchange = locationdata['Latitude'].diff()
    longchange = locationdata['Longitude'].diff()

    ###conversion rates
    ###Latitude: 1deg = 110.574 km
    ###Longitude: 1 deg = 111.320 * cos(latitude) km
    ###take a constant for longitude instead of trying to vary based on latitude
    longchange = longchange * 111320 * np.cos(0.925025)
    latchange = latchange * 110574

    ###return the changes in lat and longitude and find the distance between the two points
    diff = (pd.merge(latchange, longchange, right_index=True,
                     left_index=True)).dropna()
    diff['distance'] = [np.sqrt(x ** 2 + y ** 2) for x, y in zip(diff['Latitude'], diff['Longitude'])]

    diff.drop(diff[diff['distance'] <= 200].index, inplace=True)
    diff.drop(diff[diff['distance'] >= 100000].index, inplace=True)

    return diff['distance']


tester = journeys(36, alldata)
print(tester)


plt.hist(tester, bins=100)
plt.show()
