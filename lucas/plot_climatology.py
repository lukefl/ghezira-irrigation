import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#### PATHS ###
path_to_data = 'C:/Users/prate/Desktop/Climate Impacts Hackathon/data/era5_Geriza_Highres/'
shapefile_name = "C:/Users/prate/Desktop/Climate Impacts Hackathon/data/Gezira_shapefile/Gezira.shp"
df_shapefile = gpd.read_file(shapefile_name, crs="epsg:4326")

#### FUNCTIONS ####
def mask_region(arr,ds='era5'):
    if ds=='era5':
        arr = arr.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude")
    elif ds=='tc':
        arr = arr.rio.set_spatial_dims(x_dim="lon", y_dim="lat")
    arr = arr.rio.write_crs("epsg:4326")
    return arr.rio.clip(df_shapefile.geometry.values, df_shapefile.crs, drop = False, invert = False)


def plot(era5, title, unit, label):
    plt.figure(figsize=(10,5))
    clim = np.nanmean(era5,axis=0)
    max=np.nanmax(era5,axis=0)
    min=np.nanmin(era5,axis=0)
    time=np.arange(days)
    plt.plot(time,clim,label=label)
    plt.fill_between(time,min,max,alpha=0.5)

    plt.grid()
    plt.xlim(0,364)
    plt.legend()
    plt.xlabel('Days since January 1st')
    plt.title(f'Mean Regional {title} Climatology {start}-{end-1} ({unit})')


# initialize arrays for terraclim data
start, end = 1980, 2011
yrs = end - start
days = 365

tp_tc=np.empty((yrs, days))
rh_tc=np.empty((yrs, days))
t2m_tc=np.empty((yrs, days))

tp_tc[:]=np.nan
rh_tc[:]=np.nan
t2m_tc[:]=np.nan

print('loading terraclim...')
f_tp = xr.open_dataset(path_to_data+f"precip.e5.daily.highres.{start}-{end-1}.nc")
f_rh = xr.open_dataset(path_to_data+f"RH.e5.daily.highres.{start}-{end-1}.nc")
f_tmax = xr.open_dataset(path_to_data+f"tmax.e5.daily.highres.{start}-{end-1}.nc")
f_tmin = xr.open_dataset(path_to_data+f"tmin.e5.daily.highres.{start}-{end-1}.nc")

tp=f_tp.tp * 1000 # do unit conversion
tp.attrs['units'] = 'mm/day' # update the unit attributes
tp = mask_region(tp,ds='tc')
rh= mask_region(f_rh.relative_humidity,ds='tc')
tmax= mask_region(f_tmax.t2m,ds='tc')
tmin= mask_region(f_tmin.t2m,ds='tc')
t2m = (tmax + tmin) / 2


# Check that shapefile is working 
rh[0].plot()
plt.show()

for year in range(start, end):
    j = year - start 
    for i in range(days):
        k = i + j * 365
        tp_tc[j,i] = np.nanmean(tp[k,:,:])
        rh_tc[j,i] = np.nanmean(rh[k,:,:])
        t2m_tc[j,i] = np.nanmean(t2m[k,:,:])

plot(tp_tc, 'Daily Precipitation', 'mm/day', 'TerraClim')
plot(rh_tc, 'Relative Humidity', '%', 'TerraClim')
plot(t2m_tc, '2m Temperature', 'K', 'TerraClim')
plt.show()