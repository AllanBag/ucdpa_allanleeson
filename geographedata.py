import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import osmnx as ox
import numpy as np
import seaborn as sns
import glob
import os


###pull the dublin shape file
gdf = ox.geocode_to_gdf({'city': 'Dublin'})


#define where to find the datasets
path = 'C:\\Users\\Allan\PycharmProjects\mobyproject\\2020'
csv_files = glob.glob(os.path.join(path, "*.csv"))
alldata= pd.DataFrame()

for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)
    # append the content
    alldata = pd.concat([alldata, df])


###remove bikes reading lat 0, long 0
alldata.drop(alldata[alldata['Latitude'] == 0].index, inplace=True)
alldata.drop(alldata[alldata['Longitude'] == 0].index, inplace=True)


###choose a given hour of the day
alldata['Time'] = pd.to_datetime(alldata['HarvestTime'])
alldata['Time'] = alldata['Time'].dt.hour
alldata = alldata.loc[alldata['Time'] ==20]


####plot the shape of dublin, then the resulting data
gdf.plot(color="lightgrey")
plt.scatter(alldata['Longitude'],alldata['Latitude'], s=5, marker='.')
plt.show()