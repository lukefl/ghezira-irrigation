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

### USER SETTINGS ###
name = 'precip'
# open shapefile

file_in = "./data/Gezira_shapefile/Gezira.shp"
df_shapefile = gpd.read_file(file_in, crs="epsg:4326")
df_shapefile.plot()
#name_to_var={'precip':'tp'}
#cfactors={'precip':1000}
#units={'precip':'mm/day'}
var_clim=np.zeros(365)
counter=np.zeros(365)
# open ERA5 data sample
for year in range(1980,2011):
    f = xr.open_dataset(f"era5_data/precip/e5.{var}.daily.1990.nc")
    var=f.tp
    for i in range(365):  # how to deal with leap years??
        var = var.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude")
        var = var.rio.write_crs("epsg:4326")
        var = var.rio.clip(df_shapefile.geometry.values, df_shapefile.crs, drop = False, invert = False)
        var_clim[i] += np.nanmean(var[i,:,:],axes=(1,2))
        counter[i] += 1

var_clim = np.divide(var_clim / counter)
time=np.arange(365)
plt.figure(figsize=(10,5))
plt.plot(time,var)
