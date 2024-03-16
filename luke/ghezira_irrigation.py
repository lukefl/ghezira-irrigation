#%%
# import modules
import xarray as xr
from xclim import sdba
from xclim.core.calendar import convert_calendar
import xclim.indices as xci
import xclim.ensembles as xce
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import ec3
import gcsfs
import zarr
import cartopy.crs as ccrs

#%%
# load data
data_dir = f'/Users/lfl/utcdw_data'
RH_fname = f'RH.e5.daily.highres.1980-2010.nc'
tmin_fname = f'tmin.e5.daily.highres.1980-2010.nc'
tmax_fname = f'tmax.e5.daily.highres.1980-2010.nc'
precip_fname = f'precip.e5.daily.highres.1980-2010.nc'
tmin = xr.open_dataset(f'{data_dir}/{tmin_fname}')
tmax = xr.open_dataset(f'{data_dir}/{tmax_fname}')
RH = xr.open_dataset(f'{data_dir}/{RH_fname}')
tmax = xr.open_dataset(f'{data_dir}/{tmax_fname}')

lat = tmin.lat
lon = tmin.lon
time = tmin.time

# q_fname = 
# pr_fname = 
# xr.open_dataset(f'{data_dir}/

#%%
proj = ccrs.PlateCarree()
f, ax = plt.subplots(subplot_kw={'projection': proj},
    constrained_layout=True,figsize=(8,12))
ax.contourf(lon, lat, tmin.t2m.isel(time=0))
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

#%%
lat_bnds = [10,20]
lon_bnds = [30,40]
years_hist = np.arange(1980, 2011, 1)
years_ = np.arange(1980, 2011, 1)
lon_bnds360 = [l + 360 for l in lon_bnds]
url_gcsfs_catalog = 'https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv'

# download the CESM2 model data from Google Cloud - this code is mostly the same as 6.1

# open the Google Cloud model data catalog with pandas
df_catalog = pd.read_csv(url_gcsfs_catalog)

# search for our selected model, both historical and SSP3-7.0 scenarios
search_string = "table_id == 'day' & source_id == 'CESM2' & variable_id == 'tas'" # continue on the next line
search_string += " & experiment_id == ['historical', 'ssp370']"
df_search = df_catalog.query(search_string)

# filter the search results further for the ensemble member we want to use
df_search_r10i1p1f1 = df_search.query("member_id == 'r10i1p1f1'")

# authenticate access to Google Cloud
gcs = gcsfs.GCSFileSystem(token='anon')

# get the URLs for each dataset and turn into zarr store mappers
url_hist = df_search_r10i1p1f1[df_search_r10i1p1f1.experiment_id == 'historical'].zstore.values[0]
mapper_hist = gcs.get_mapper(url_hist)
url_ssp3 = df_search_r10i1p1f1[df_search_r10i1p1f1.experiment_id == 'ssp370'].zstore.values[0]
mapper_ssp3 = gcs.get_mapper(url_ssp3)

# download the datasets, subset, and convert units
# historical
ds_hist_raw = xr.open_zarr(mapper_hist, consolidated = True)
tas_hist_raw = ds_hist_raw.tas.sel(lat = slice(*lat_bnds), lon = slice(*lon_bnds360)) - 273.15 # also convert to C

# future
ds_ssp3_raw = xr.open_zarr(mapper_ssp3, consolidated = True)
tas_ssp3_raw = ds_ssp3_raw.tas.sel(lat = slice(*lat_bnds), lon = slice(*lon_bnds360)) - 273.15 

# select time periods
tas_hist_raw = tas_hist_raw.sel(time = tas_hist_raw.time.dt.year.isin(years_hist))
tas_ssp3_raw = tas_ssp3_raw.sel(time = tas_ssp3_raw.time.dt.year.isin(years_future))
# %%
