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
path_to_data = 'C:/Users/prate/Desktop/Climate Impacts Hackathon/data/era5_Geriza_Highres/'

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
    min=mod.groupby('time.dayofyear').max(dim='time')
    time=np.arange(365)
    clim.plot(label='CESM')
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
f_precip = xr.open_dataset(path_to_data+f"precip.e5.daily.highres.{start}-{end-1}.nc")
f_rhumid = xr.open_dataset(path_to_data+f"RH.e5.daily.highres.{start}-{end-1}.nc")
f_tmax = xr.open_dataset(path_to_data+f"tmax.e5.daily.highres.{start}-{end-1}.nc")
f_tmin = xr.open_dataset(path_to_data+f"tmin.e5.daily.highres.{start}-{end-1}.nc")

precip_obs=f_precip.tp * 1000 # do unit conversion
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

temp_obs = (tmax + tmin) / 2

print('loading cesm...')
precip_mod=load_var('pr',experiment_id='historical',years=np.arange(start,end)) / 997  # do unit conversion
print('loaded precip...')
rhumid_mod=load_var('hur',experiment_id='historical',years=np.arange(start,end))* 100
print('loaded humidity...')
temp_mod=load_var('tas',experiment_id='historical',years=np.arange(start,end))
print('loaded temp...')


# precip_mod.attrs['units'] = 'mm/day' # update the unit attributes
precip_mod=mask_region_cesm(precip_mod)
precip_mod=precip_mod.mean(dim=('lat','lon'))
print(np.shape(precip_mod))
print('meaned precip...')

rhumid_mod=mask_region_cesm(rhumid_mod) 
rhumid_mod=rhumid_mod.sel(plev=1000,method='nearest').mean(dim=('lat','lon'))
print('meaned humidity...')

temp_mod=mask_region_cesm(temp_mod)
temp_mod=temp_mod.mean(dim=('lat','lon'))
print('meaned temp...')

print('plotting...')
plot(precip_obs, precip_mod, 'Daily Precipitation', 'mm/day')
plot(rhumid_obs, rhumid_mod, 'Relative Humidity', '%')
plot(temp_obs, temp_mod, 'Surface Air Temperature', 'K')
# plot(revap_obs, revap_mod,'Reference Evapotransporation', 'K')
plt.show()