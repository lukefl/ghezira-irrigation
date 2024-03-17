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

#### PATHS ###
path_to_downscaled = 'C:/Users/prate/Desktop/Climate Impacts Hackathon/data/downscaled/'

# SETTINGS
forcing = 'his' # or '370'
bias_correction='dbcca' # or 'bcca'
efficiency=0.55

f_precip = xr.open_dataset(path_to_downscaled+f"pr.{forcing}.{bias_correction}.nc")
f_rhumid = xr.open_dataset(path_to_downscaled+f"hur.{forcing}.{bias_correction}.nc")
f_temp = xr.open_dataset(path_to_downscaled+f"tas.{forcing}.{bias_correction}.nc")
                         
precip_mod=mask_region(f_precip.pr) * 3600 * 24
precip_mod=precip_mod.mean(dim=('lat','lon'))

rhumid_mod=mask_region(f_rhumid.hur) * 100
rhumid_mod=rhumid_mod.mean(dim=('lat','lon'))

temp_mod=mask_region(f_temp.tas)
temp_mod=temp_mod.mean(dim=('lat','lon')) 

revap_mod=reference_crop_evapotranspiration(temp_mod,rhumid_mod)

CROPS = [WHEAT, SORGHUM, GROUNDNUTS, COTTON]
LANDUSE = [0.39, 0.37, 0.15, 0.09]
area = 750000 * 10000 # convert ha to m^2
daily_water_use = np.zeros_like(temp_mod)
for i in range(4):
    daily_water_use += irrigation_water_demand(CROPS[i], temp_mod, rhumid_mod, precip_mod, efficiency) * area * LANDUSE[i]
daily_water_use /= 1000  # convert from mm*m^2 to m^3

annual_water_use = daily_water_use.groupby('time.year').sum(dim='time.year')
mean_annual_water_use = annual_water_use.mean()
print(mean_annual_water_use)