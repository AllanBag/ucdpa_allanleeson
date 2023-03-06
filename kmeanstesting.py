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

####plot the shape of dublin, then the resulting data
gdf.plot(color="lightgrey")
plt.scatter(alldata['Longitude'],alldata['Latitude'], s=5, marker='.')
plt.show()
print(alldata)

x=pd.DataFrame()
x['Longitude']= alldata['Longitude']
x['Latitude'] = alldata['Latitude']


####Elbow test- Find optimal cluster amount
#initialize kmeans parameters
kmeans_kwargs = {
"init": "random",
"n_init": 10,
"random_state": 1,
}
#create list to hold SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(x)
    sse.append(kmeans.inertia_)
#visualize results
plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.xlabel("No of Clusters")
plt.ylabel("SSE")
plt.show()

#####kmeans test- n_clusters being number of clusters recommended by the elbow test (3)
kmeans = KMeans(n_clusters=3)
kmeans.fit_predict(x)

###acquire anomaly score- ie, the minimum distance between a given point and the nearest cluster. becomes very apparent if we increase the amount of clusters
x['anomaly'] = kmeans.transform(x).min(axis=1)

#get cluster centres and plot the dublin map
gdf.plot(color="lightgrey")
centroids = kmeans.cluster_centers_
centroids_x = centroids[:,0]
centroids_y = centroids[:,1]
print(x)

####plot it all
plt.scatter(x['Longitude'], x['Latitude'], c=x['anomaly'], cmap='coolwarm', s=6)
plt.colorbar(label = 'Anomaly Score')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.scatter(centroids_x, centroids_y, marker='h', color = 'red')
plt.show()