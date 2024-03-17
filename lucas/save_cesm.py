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

path='C:/Users/prate/Desktop/Climate Impacts Hackathon/data/cesm/'
experiment='ssp370' #ssp585 or historical
start, end = 2070, 2101
arr=load_var('pr',experiment_id=experiment,years=np.arange(start,end),member_id='r4i1p1f1') #.sel(plev=1000,method='nearest')
print('loaded var')
arr.to_netcdf(path+f'pr.cesm.daily.{experiment}.{start}-{end-1}.nc','w')
arr.close()