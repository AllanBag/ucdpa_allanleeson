import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import osmnx as ox
import numpy as np
import glob
from sklearn.cluster import KMeans
import os


###pull the dublin shape file
gdf = ox.geocode_to_gdf({'city': 'Dublin'})

#define where to find the datasets
path = 'C:\\Users\\Allan\PycharmProjects\mobyproject\\2022'
csv_files = glob.glob(os.path.join(path, "*.csv"))
alldata= pd.DataFrame()

for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)
    # append the content
    alldata = pd.concat([alldata, df])

#path = 'C:\\Users\\Allan\PycharmProjects\mobyproject\\2021'
#csv_files = glob.glob(os.path.join(path, "*.csv"))

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
print(len(alldata))

x=pd.DataFrame()
x['Longitude']= alldata['Longitude']
x['Latitude'] = alldata['Latitude']

#####kmeans test- n_clusters being number of clusters
kmeans = KMeans(n_clusters=2)
kmeans.fit(x)

#get cluster centres
gdf.plot(color="lightgrey")
centroids = kmeans.cluster_centers_
centroids_x = centroids[:,0]
centroids_y = centroids[:,1]

####plot it all
plt.scatter(alldata['Longitude'],alldata['Latitude'], s=5, marker='.')
plt.scatter(centroids_x, centroids_y, marker='h', color = 'red')
plt.show()

