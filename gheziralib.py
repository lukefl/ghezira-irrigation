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

def load_var(
    var,member_id='r10i1p1f1',experiment_id='ssp370',lon_bnds=[30,40],
    lat_bnds=[10,20],years=np.arange(2070, 2100, 1),
    source_id='CESM2',table_id='day'
    ):
    # download the CESM2 model data from Google Cloud - this code is mostly the same as 6.1

    # URL for the Google Cloud model data catalog
    url_gcsfs_catalog = 'https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv'
    # lon_bnds360 = [l + 360 for l in lon_bnds]

    # open the Google Cloud model data catalog with pandas
    df_catalog = pd.read_csv(url_gcsfs_catalog)

    # search for our selected model, both historical and SSP3-7.0 scenarios
    search_string = f"table_id == '{table_id}' & source_id == '{source_id}' & variable_id == '{var}'" # continue on the next line
    search_string += f" & experiment_id == '{experiment_id}'"
    df_search = df_catalog.query(search_string)

    # filter the search results further for the ensemble member we want to use
    df_search_member = df_search.query(f"member_id == '{member_id}'")

    # authenticate access to Google Cloud
    gcs = gcsfs.GCSFileSystem(token='anon')

    # get the URLs for each dataset and turn into zarr store mappers
    # url_hist = df_search_member[df_search_member.experiment_id == 'historical'].zstore.values[0]
    # mapper_hist = gcs.get_mapper(url_hist)
    # url_ssp3 = df_search_member[df_search_member.experiment_id == f'{experiment_id}'].zstore.values[0]
    url = df_search_member[df_search_member.experiment_id == f'{experiment_id}'].zstore.values[0]
    mapper = gcs.get_mapper(url)

    # future
    ds_raw = xr.open_zarr(mapper, consolidated = True)
    var_raw = ds_raw[f'{var}'].sel(lat = slice(*lat_bnds), lon = slice(*lon_bnds)) - 273.15 

    # select time periods
    # var_hist_raw = var_hist_raw.sel(time = var_hist_raw.time.dt.year.isin(years_hist))
    var_raw = var_raw.sel(time = var_raw.time.dt.year.isin(years))
    return var_raw

#%%
# test function
# tas_hist_raw, tas_ssp3_raw = load_var('tas')
tas_ssp3_raw = load_var('tas')
