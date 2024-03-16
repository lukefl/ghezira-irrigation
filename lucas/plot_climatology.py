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
path_to_obs = 'C:/Users/prate/Desktop/Climate Impacts Hackathon/data/era5_Geriza_Highres/'
path_to_mod = 'C:/Users/prate/Desktop/Climate Impacts Hackathon/data/cesm/'

#### FUNCTIONS ####
def plot(obs, mod, title, unit):
    print(f'plotting {title} obs...')
    plt.figure(figsize=(10,5))
    clim = obs.groupby('time.dayofyear').mean(dim='time')
    max=obs.groupby('time.dayofyear').max(dim='time')
    min=obs.groupby('time.dayofyear').min(dim='time')
    time=np.arange(366)
    clim.plot(label='TerraClim')
    plt.fill_between(time,min,max,alpha=0.5)
    
    print(f'plotting {title} model...')
    clim = mod.groupby('time.dayofyear').mean(dim='time')
    max=mod.groupby('time.dayofyear').max(dim='time')
    min=mod.groupby('time.dayofyear').min(dim='time')
    time=np.arange(365)
    clim.plot(label='CESM Historical Data')
    plt.fill_between(time,min,max,alpha=0.5)

    plt.grid()
    plt.xlim(0,365)
    plt.legend()
    plt.xlabel('Days since January 1st')
    plt.title(f'Mean Regional {title} Climatology {start}-{end-1} ({unit})')


# initialize arrays for terraclim data
start, end = 1980, 2011
yrs = end - start
days = 365

print('loading terraclim...')
f_precip = xr.open_dataset(path_to_obs+f"precip.e5.daily.highres.{start}-{end-1}.nc")
f_rhumid = xr.open_dataset(path_to_obs+f"RH.e5.daily.highres.{start}-{end-1}.nc")
f_tmax = xr.open_dataset(path_to_obs+f"tmax.e5.daily.highres.{start}-{end-1}.nc")
f_tmin = xr.open_dataset(path_to_obs+f"tmin.e5.daily.highres.{start}-{end-1}.nc")

precip_obs=f_precip.tp #* 1000 # do unit conversion
precip_obs.attrs['units'] = 'mm/day' # update the unit attributes
precip_obs = mask_region(precip_obs)
precip_obs=precip_obs.mean(dim=('lat','lon'))

print(np.shape(precip_obs))
rhumid_obs= mask_region(f_rhumid.relative_humidity) 
rhumid_obs= rhumid_obs.mean(dim=('lat','lon'))

tmax= mask_region(f_tmax.t2m)
tmax=tmax.mean(dim=('lat','lon'))

tmin= mask_region(f_tmin.t2m)
tmin=tmin.mean(dim=('lat','lon'))

temp_obs = (tmax + tmin) / 2  + 273.15

print('loading cesm...')
f_precip = xr.open_dataset(path_to_mod+f"precip.cesm.daily.historical.{start}-{end-1}.nc")
f_rhumid = xr.open_dataset(path_to_mod+f"RH.cesm.daily.historical.{start}-{end-1}.nc")
f_temp = xr.open_dataset(path_to_mod+f"tas.cesm.daily.historical.{start}-{end-1}.nc")

# precip_mod.attrs['units'] = 'mm/day' # update the unit attributes
precip_mod=mask_region_cesm(f_precip.pr) * 3600 * 24
precip_mod=precip_mod.mean(dim=('lat','lon'))
print(np.shape(precip_mod))
print('meaned precip...')

rhumid_mod=mask_region_cesm(f_rhumid.hur) * 100
rhumid_mod=rhumid_mod.mean(dim=('lat','lon'))
print('meaned humidity...')

temp_mod=mask_region_cesm(f_temp.tas)
temp_mod=temp_mod.mean(dim=('lat','lon'))
print('meaned temp...')

#%%
print('plotting...')
plot(precip_obs, precip_mod, 'Daily Precipitation', 'mm/day')
plot(rhumid_obs, rhumid_mod, 'Relative Humidity', '%')
plot(temp_obs, temp_mod, 'Surface Air Temperature', 'K')
# plot(revap_obs, revap_mod,'Reference Evapotransporation', 'K')
plt.show()