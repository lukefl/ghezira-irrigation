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
path_to_downscaled = 'C:/Users/prate/Desktop/Climate Impacts Hackathon/data/cesm/'

# SETTINGS
forcing = 'his' # or '370'
bias_correction='dbcca' # or 'bcca'
efficiency=0.55

f_precip = xr.open_dataset(path_to_downscaled+f"precip.cesm.daily.historical.1980-2010.nc")
f_rhumid = xr.open_dataset(path_to_downscaled+f"RH.cesm.daily.historical.1980-2010.nc")
f_temp = xr.open_dataset(path_to_downscaled+f"tas.cesm.daily.historical.1980-2010.nc")
                         
precip_mod=mask_region_cesm(f_precip.pr) * 3600 * 24

rhumid_mod=mask_region_cesm(f_rhumid.hur) * 100

temp_mod=mask_region_cesm(f_temp.tas)

revap_mod=reference_crop_evapotranspiration(temp_mod,rhumid_mod)

CROPS = [WHEAT, SORGHUM, GROUNDNUTS, COTTON]
LANDUSE = [0.39, 0.37, 0.15, 0.09]
area = 750000 * 10000 # convert ha to m^2
daily_water_use = np.zeros_like(temp_mod)
for i in range(4):
    daily_water_use += irrigation_water_demand(CROPS[i], temp_mod, rhumid_mod, precip_mod, efficiency) * area * LANDUSE[i]
daily_water_use /= 1000  # convert from mm*m^2 to m^3 / day
daily_water_use = daily_water_use.mean(dim=('lat','lon'))

print(daily_water_use.groupby('time.year').dims)
annual_water_use = daily_water_use.groupby('time.year').sum(dim='time')
print(annual_water_use.dims)
mean_annual_water_use = annual_water_use.mean(dim='year')
print(mean_annual_water_use.data / (1000)**3) # cubic km / year