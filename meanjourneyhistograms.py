import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import re
import statistics as stat
###comments

path = 'C:\\Users\\Allan\PycharmProjects\mobyproject\\2020\\'
csv_files = glob.glob(os.path.join(path, "*.csv"))

# loop over the list of csv files
alldata = pd.DataFrame()

for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)
    # append the content
    alldata = pd.concat([alldata, df])
print(len(alldata))

#####Remove bikes with location "0", ie offline readings and add column for hour data collected in
alldata.drop(alldata[alldata['Latitude'] == 0].index, inplace=True)
alldata['Time'] = pd.to_datetime(alldata['HarvestTime'])
alldata['Time'] = alldata['Time'].dt.hour
print(len(alldata))

####to check given date across all dataset if necessary, pulls out the year from all harvesttime filestamps. Should be consistent across all rows if you're pulling the year's data
###My apologies, I really didn't find a use case for a Regex in this project!
def get_year(date):
    return re.search(r"\d{4}", date).group(0)

def bikeselect(bikeno, dataset):
    ######to find a given bikes journeys, and remove periods where the bike was stationary
    bikedata = dataset.loc[dataset['BikeID'] == bikeno]
    bikedata = bikedata.drop_duplicates(['Latitude', 'Longitude'], keep='last')
    return (bikedata)


def journeys(bikeno, dataset):
    ###returns distance travelled for a given BikeID
    locationdata = bikeselect(bikeno, dataset)
    latchange = locationdata['Latitude'].diff()
    longchange = locationdata['Longitude'].diff()

    ###conversion rates
    ###Latitude: 1deg = 110.574 km
    ###Longitude: 1 deg = 111.320 * cos(latitude) km
    ###take a constant for longitude instead of trying to vary based on latitude (latitude expressed in radians)
    longchange = longchange * 111320 * np.cos(0.925025)
    latchange = latchange * 110574

    ###return the changes in lat and longitude and find the distance between the two points,looping for all values)
    diff = (pd.merge(latchange, longchange, right_index=True,
                     left_index=True)).dropna()
    diff['distance'] = [np.sqrt(x ** 2 + y ** 2) for x, y in zip(diff['Latitude'], diff['Longitude'])]

    ####Remove outlier journeys- Those short enough to be times where the bike was physically moved/dragged despite its lock or went offline before being moved
    diff.drop(diff[diff['distance'] <= 100].index, inplace=True)
    diff.drop(diff[diff['distance'] >= 100000].index, inplace=True)
    return diff['distance']

#####Initialise a dataframe and get a some of all BikeIDs (allbikes)
alljourneysinyear = pd.DataFrame()
allbikes= alldata['BikeID'].unique()

###Analyse all bike IDs to get all journeys in given year
for bike in allbikes:
    bikeselected = journeys(bike,alldata)
    bikeselected = pd.DataFrame(bikeselected)
    alljourneysinyear = pd.concat([bikeselected, alljourneysinyear], axis=0)

###get the mean journey and variance
avjourney = int(np.median(alljourneysinyear['distance']))
stdjourney = int(np.var(alljourneysinyear['distance']))

###pull out the year from the dataset
year = get_year(alldata['HarvestTime'].iloc[5])

####putting it together
plt.hist(alljourneysinyear, bins=30)
plt.xlabel('Metres')
plt.ylabel('Number of Journeys')
plt.show()



print('In '+ str(year)+' the mean journey length was ' +str(avjourney)+' m with variance '+str(stdjourney))
