#%%
import os
os.chdir('/Users/lfl/google_drive/phd/utcdw_hackathon/ghezira-irrigation')
print(os.getcwd())
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import importlib
# importlib.reload(sys.modules['gheziralib'])
import sys
sys.path.append('/Users/lfl/google_drive/phd/utcdw_hackathon/'+ 
    'ghezira-irrigation/')
import gheziralib as gl
sys.path.append('/Users/lfl/google_drive/phd/utcdw_hackathon/UTCDW_Guidebook/' +
                'downscaling_code')
from DBCCA import DBCCA
import xesmf as xe
#%%
yri_obs = 1980
yrf_obs = 2011
# set paths
path_to_data = '/Users/lfl/utcdw_data/'
data_transfer = ('/Users/lfl/google_drive/phd/utcdw_hackathon/' +
    'ghezira-irrigation/data-transfer')

# model data file names
tas_his_fname = 'tas.cesm.daily.historical.1980-2010.nc'
tas_370_fname = 'tas.cesm.daily.ssp370.2070-2100.nc'
pr_his_fname = 'precip.cesm.daily.historical.1980-2010.nc'
pr_370_fname = 'pr.cesm.daily.ssp370.2070-2100.nc'
hur_his_fname = 'RH.cesm.daily.historical.1980-2010.nc'
hur_370_fname = 'RH.cesm.daily.ssp370.2070-2100.nc'

# obs file names
tmax_obs_fname = f"tmax.e5.daily.highres.{yri_obs}-{yrf_obs-1}.nc"
tmin_obs_fname = f"tmin.e5.daily.highres.{yri_obs}-{yrf_obs-1}.nc"
pr_obs_fname = f"precip.e5.daily.highres.{yri_obs}-{yrf_obs-1}.nc"
hur_obs_fname = f"RH.e5.daily.highres.{yri_obs}-{yrf_obs-1}.nc"

#  output file names
tas_his_bcca_file = f'{path_to_data}tas_his_bcca.nc'
tas_370_bcca_file = f'{path_to_data}tas_370_bcca.nc'
tas_his_dbcca_file = f'{path_to_data}tas_his_dbcca.nc'
tas_370_dbcca_file = f'{path_to_data}tas_370_dbcca.nc'

pr_his_bcca_file = f'{path_to_data}pr_his_bcca.nc'
pr_370_bcca_file = f'{path_to_data}pr_370_bcca.nc'
pr_his_dbcca_file = f'{path_to_data}pr_his_dbcca.nc'
pr_370_dbcca_file = f'{path_to_data}pr_370_dbcca.nc'

hur_his_bcca_file = f'{path_to_data}hur_his_bcca.nc'
hur_370_bcca_file = f'{path_to_data}hur_370_bcca.nc'
hur_his_dbcca_file = f'{path_to_data}hur_his_dbcca.nc'
hur_370_dbcca_file = f'{path_to_data}hur_370_dbcca.nc'

#%%
# load CESM data
tas_his = xr.load_dataset(f'{data_transfer}/{tas_his_fname}').tas
tas_370 = xr.load_dataset(f'{data_transfer}/{tas_370_fname}').tas
#
pr_his = xr.load_dataset(f'{data_transfer}/{pr_his_fname}').pr
pr_370 = xr.load_dataset(f'{data_transfer}/{pr_370_fname}').pr
#
# hur_his = xr.load_dataset(f'{data_transfer}/{hur_his_fname}').hur
# hur_370 = xr.load_dataset(f'{data_transfer}/{hur_370_fname}').hur

#%%
# load obs
f_tmax = (xr.open_dataset(f"{path_to_data}/{tmax_obs_fname}")
    .convert_calendar('noleap').drop_vars(['time_level_0','time_level_1']))
f_tmin = (xr.open_dataset(f"{path_to_data}/{tmin_obs_fname}")
    .convert_calendar('noleap').drop_vars(['time_level_0','time_level_1']))
f_pr = (xr.open_dataset(f"{path_to_data}/{pr_obs_fname}")
    .convert_calendar('noleap').drop_vars(['time_level_0','time_level_1']))
f_hur = (xr.open_dataset(f"{path_to_data}/{hur_obs_fname}")
    .convert_calendar('noleap'))
tas_obs = (f_tmax.t2m + f_tmin.t2m) / 2
pr_obs = f_pr.tp
hur_obs = f_hur.relative_humidity
#%%
# regrid obs to CESM grid
regridder = xe.Regridder(tas_obs, tas_his, "bilinear")
tas_obs_coarse = regridder(tas_obs)
pr_obs_coarse = regridder(pr_obs)
hur_obs_coarse = regridder(hur_obs)

#%%
# do dbcca on tas and pr
# # tas
# DBCCA(
#     tas_his, tas_370, tas_obs_coarse, tas_obs, n_analogues=30,
#     window_size=45, window_unit='days', write_output=True, do_future=True,
#     fout_hist_bcca=tas_his_bcca_file, fout_future_bcca=tas_370_bcca_file,
#     fout_hist_dbcca=tas_his_dbcca_file, fout_future_dbcca=tas_370_dbcca_file
#     )
# tas
DBCCA(
    pr_his, pr_370, pr_obs_coarse, pr_obs, n_analogues=30,
    window_size=45, window_unit='days', write_output=True, do_future=True,
    fout_hist_bcca=pr_his_bcca_file, fout_future_bcca=pr_370_bcca_file,
    fout_hist_dbcca=pr_his_dbcca_file, fout_future_dbcca=pr_370_dbcca_file
    )
