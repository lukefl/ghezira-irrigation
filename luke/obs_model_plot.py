#%%
import os
os.chdir('/Users/lfl/google_drive/phd/utcdw_hackathon/ghezira-irrigation')
import numpy as np
# import pandas as pd
# import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
# import rioxarray as rxr
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
import importlib
importlib.reload(sys.modules['gheziralib'])
import gheziralib as gl
#%%
#### PATHS ###
path_to_data = '/Users/lfl/utcdw_data/'
# shapefile_name = f"{path_to_data}/Gezira.shp"
# df_shapefile = gpd.read_file(shapefile_name, crs="epsg:4326")

#%%
# load CESM data
years_hist = np.arange(1980,2010, 1)
years_585 = np.arange(2070, 2100, 1)
tas = gl.load_var(
    var='tas',experiment_id='historical', years=years_hist)
# pr = gl.load_var(
#     var='pr',experiment_id='historical', years=years_hist)
# hur = gl.load_var(
#     var='hur',experiment_id='historical', years=years_hist)
#%%
# def plot(dat, title, unit, label):
#     plt.figure(figsize=(10,5))
#     clim = np.nanmean(dat,axis=0)
#     max=np.nanmax(dat,axis=0)
#     min=np.nanmin(dat,axis=0)
#     time=np.arange(days)
#     plt.plot(time,clim,label=label)
#     plt.fill_between(time,min,max,alpha=0.5)

#     plt.grid()
#     plt.xlim(0,364)
#     plt.legend()
#     plt.xlabel('Days since January 1st')
#     plt.title(f'Mean Regional {title} Climatology {start}-{end-1} ({unit})')

#%%
# initialize arrays for terraclim data
start, end = 1980, 2011
yrs = end - start
days = 365

# tp_tc=np.empty((yrs, days))
# rh_tc=np.empty((yrs, days))
# t2m_tc=np.empty((yrs, days))
# re_tc=np.empty((yrs, days))

# tp_tc[:]=np.nan
# rh_tc[:]=np.nan
# t2m_tc[:]=np.nan
# re_tc[:]=np.nan

print('loading terraclim...')
f_precip = xr.open_dataset(path_to_data+f"precip.e5.daily.highres.{start}-{end-1}.nc")
f_rh = xr.open_dataset(path_to_data+f"RH.e5.daily.highres.{start}-{end-1}.nc")
f_tmax = xr.open_dataset(path_to_data+f"tmax.e5.daily.highres.{start}-{end-1}.nc")
f_tmin = xr.open_dataset(path_to_data+f"tmin.e5.daily.highres.{start}-{end-1}.nc")

precip=f_precip.tp * 1000 # do unit conversion
precip.attrs['units'] = 'mm/day' # update the unit attributes
precip = gl.mask_region(
    precip,x_dim='lon',y_dim='lat',shapefile_name=f"{path_to_data}/Gezira.shp")
# rh= gl.mask_region(f_rh.relative_humidity,xdim='lon',ydim='lat')
# tmax= gl.mask_region(f_tmax.t2m,xdim='lon',ydim='lat')
# tmin= gl.mask_region(f_tmin.t2m,xdim='lon',ydim='lat')
# t2m = (tmax + tmin) / 2

#%%
# Check that shapefile is working 
#rh[0].plot()
#plt.show()

for year in range(start, end):
    j = year - start 
    for i in range(days):
        k = i + j * 365
        tp_tc[j,i] = np.nanmean(tp[k,:,:])
        rh_tc[j,i] = np.nanmean(rh[k,:,:])
        t2m_tc[j,i] = np.nanmean(t2m[k,:,:])
        re_tc[j,i] = reference_crop_evapotranspiration(t2m_tc[j,i], rh_tc[j,i])

plot(tp_tc, 'Daily Precipitation', 'mm/day', 'TerraClim')
plot(rh_tc, 'Relative Humidity', '%', 'TerraClim')
plot(t2m_tc, '2m Temperature', 'K', 'TerraClim')
plot(re_tc, 'Reference Evapotransporation', 'K', 'TerraClim')
plt.show()
# %%
