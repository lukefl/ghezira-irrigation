#%%
# import modules
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xesmf as xe
import xclim.sdba as sdba

name = 'precip'

#%%
# open shapefile
data_dir = f'/Users/lfl/utcdw_data'

file_in = f"{data_dir}/Gezira.shp"

df_shapefile = gpd.read_file(file_in, crs="epsg:4326")
df_shapefile.plot()

def mask_region(arr,xdim,ydim):
    arr = arr.rio.set_spatial_dims(x_dim=xdim, y_dim=ydim)
    arr = arr.rio.write_crs("epsg:4326")
    return arr.rio.clip(df_shapefile.geometry.values, df_shapefile.crs, drop = False, invert = False)

# start, end = 1980, 2011
yrs = end - start
days = 365
tmin_dat=np.empty((yrs, days))
rh_dat=np.empty((yrs, days))
tmax_dat=np.empty((yrs, days))

tmin_dat[:]=np.nan
rh_dat[:]=np.nan
tmax_dat[:]=np.nan

#%%
# test for relative humidity
rh_file = f"RH.e5.daily.highres.1980-2010.nc"
tmin_file = f"tmin.e5.daily.highres.1980-2010.nc"
tmax_file = f"tmax.e5.daily.highres.1980-2010.nc"
precip_file = f"precip.e5.daily.highres.1980-2010.nc"

f_rh = xr.open_dataset(f"{data_dir}/{rh_file}")
# f_rh.dims
rh=mask_region(f_rh.relative_humidity,xdim='lat',ydim='lon')
# rh[0].plot()

#%%
# open ERA5 data sample
# for year in range(start,end):
f_rh = xr.open_dataset(f"{data_dir}/{rh_file}")
f_tmin = xr.open_dataset(f"{data_dir}/{tmin_file}")
f_tmax = xr.open_dataset(f"{data_dir}/{tmax_file}")
# j = year - start
tmin=f_tmin.t2m * 1000 # do unit conversion
tmin.attrs['units'] = 'mm/day' # update the unit attributes
tmin = mask_region(tmin,xdim='lat',ydim='lon')
#%%
rh=mask_region(f_rh.relative_humidity,xdim='lat',ydim='lon')
tmax=mask_region(f_tmax.t2m,xdim='lat',ydim='lon')
rh_dclim = rh.groupby('time.dayofyear').mean('time')
tmax_dclim = rh.groupby('time.dayofyear').mean('time')
# for i in range(days):  # how to deal with leap years??
#     tmin_dat[j,i] = np.nanmean(tmin[i,:,:])
#     rh_dat[j,i] = np.nanmean(rh[i,:,:])
#         # t2m_dat[j,i] = np.nanmean(t2m[i,:,:])

#%%
def plot(dat, title, unit):
    clim = dat.mean(dim=['lat','lon'])
    max=dat.max
    min=dat.min
    time=clim.dayofyear
    plt.figure(figsize=(10,5))
    plt.plot(time,clim,label='ERA5')
    plt.fill_between(time,min,max,alpha=0.5)
    plt.grid()
    plt.xlim(0,364)
    plt.legend()
    plt.xlabel('Days since January 1st')
    # plt.title(f'Mean Regional {title} Climatology {start}-{end-1} ({unit})')

# plot(tmin, 'Daily Precipitation', 'mm/day')
plot(rh_dclim, 'Relative Humidity', '%')
# plot(tmax, '2m Temperature', 'K')
# %%
