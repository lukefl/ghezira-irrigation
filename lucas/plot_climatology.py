import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import cartopy.crs as ccrs
import cartopy.feature as cfeature

path_to_era5 = 'era5_Geriza'
path_to_terraclim = './data/era5_Geriza_Highres'
shapefile_name = "./data/Gezira_shapefile/Gezira.shp"
df_shapefile = gpd.read_file(shapefile_name, crs="epsg:4326")
# df_shapefile.plot()
# plt.show()

def mask_region(arr,ds='era5'):
    if ds=='era5':
        arr = arr.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude")
    elif ds=='tc':
        arr = arr.rio.set_spatial_dims(x_dim="lon", y_dim="lat")
    arr = arr.rio.write_crs("epsg:4326")
    return arr.rio.clip(df_shapefile.geometry.values, df_shapefile.crs, drop = False, invert = False)

# initialize variables for era5 data
start, end = 1980, 2011
yrs = end - start
days = 365
tp_era5=np.empty((yrs, days))
rh_era5=np.empty((yrs, days))
t2m_era5=np.empty((yrs, days))

tp_era5[:]=np.nan
rh_era5[:]=np.nan
t2m_era5[:]=np.nan

# open ERA5 data
print('load ERA5...')
for year in range(start,end):
    f_tp = xr.open_dataset(f"./data/era5_Geriza/precip/e5.precip.daily.{year}.nc")
    f_rh = xr.open_dataset(f"./data/era5_Geriza/RH/e5.RH.1000hPa.daily.{year}.nc")
    f_t2m = xr.open_dataset(f"./data/era5_Geriza/t2m/e5.t2m.daily.{year}.nc")
    j = year - start
    tp=f_tp.tp * 1000 # do unit conversion
    tp.attrs['units'] = 'mm/day' # update the unit attributes
    tp = mask_region(tp)
    rh=mask_region(f_rh.r)
    t2m=mask_region(f_t2m.t2m)
    for i in range(days):  # how to deal with leap years??
        tp_era5[j,i] = np.nanmean(tp[i,:,:])
        rh_era5[j,i] = np.nanmean(rh[i,:,:])
        t2m_era5[j,i] = np.nanmean(t2m[i,:,:])

def plot(era5, title, unit):
    plt.figure(figsize=(10,5))
    clim = np.nanmean(era5,axis=0)
    max=np.nanmax(era5,axis=0)
    min=np.nanmin(era5,axis=0)
    time=np.arange(days)
    plt.plot(time,clim,label='ERA5')
    plt.fill_between(time,min,max,alpha=0.5)

    plt.grid()
    plt.xlim(0,364)
    plt.legend()
    plt.xlabel('Days since January 1st')
    plt.title(f'Mean Regional {title} Climatology {start}-{end-1} ({unit})')

plot(tp_era5, 'Daily Precipitation', 'mm/day')
plot(rh_era5, 'Relative Humidity', '%')
plot(t2m_era5, '2m Temperature', 'K')
plt.show()