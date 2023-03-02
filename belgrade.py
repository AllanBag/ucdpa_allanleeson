import osmnx as ox
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

gdf = ox.geocode_to_gdf({'city': 'Dublin'})

gdf.plot(color="lightgrey")
plt.show()