import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys
sys.path.insert(1, 'C:/Users/prate/Desktop/Climate Impacts Hackathon/ghezira-irrigation/')
from gheziralib import *

start,end=1980,2010
temp_mod=load_var('pr',experiment_id='historical',years=np.arange(start,end))

#temp_mod[0].plot()
# latc, lonc = 14.5, 33
# rg = 1
# lat, lon = temp_mod.lat, temp_mod.lon
# latmask = np.abs(lat-latc)<rg
# lonmask = np.abs(lon-lonc)<rg
# temp_mod[0,latmask,lonmask].plot()
# temp_mod[0,3:5,2:4].plot()
temp_mod=mask_region_cesm(temp_mod)
print('masked')
mean=temp_mod.mean(dim=('lat','lon'))
print(mean)
temp_mod[0].plot()
plt.xlim(32,34.5)
plt.ylim(11,16)
plt.show()