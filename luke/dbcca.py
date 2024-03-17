#%%
import os
os.chdir('/Users/lfl/google_drive/phd/utcdw_hackathon/ghezira-irrigation')
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import importlib
# importlib.reload(sys.modules['gheziralib'])
import gheziralib as gl
import sys
sys.path.append('/Users/lfl/google_drive/phd/utcdw_hackathon/UTCDW_Guidebook/' +
                'downscaling_code')
from DBCCA import DBCCA
import xesmf as xe
#%%
# set paths
path_to_data = '/Users/lfl/utcdw_data/'
data_transfer = ('/Users/lfl/google_drive/phd/utcdw_hackathon/' +
    'ghezira-irrigation/data-transfer')

tas_his_fname = 'tas.cesm.daily.historical.1980-2010.nc'
tas_370_fname = 'tas.cesm.daily.ssp370.2070-2100.nc'
pr_his_fname = 'precip.cesm.daily.historical.1980-2010.nc'
pr_370_fname = 'precip.cesm.daily.ssp370.2070-2100.nc'
hur_his_fname = 'RH.cesm.daily.historical.1980-2010.nc'
hur_370_fname = 'RH.cesm.daily.ssp370.2070-2100.nc'

# set output file names
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
# start = 1980
# end = 2011
# years_his = np.arange(1980,2011, 1)
# years_585 = np.arange(2070, 2011, 1)
# member_id = 'r10i1p1f1'
tas_his = xr.load_dataset(f'{data_transfer}/{tas_his_fname}')
tas_370 = xr.load_dataset(f'{data_transfer}/{tas_370_fname}')
#
pr_his = xr.load_dataset(f'{data_transfer}/{pr_his_fname}')
pr_370 = xr.load_dataset(f'{data_transfer}/{pr_370_fname}')
#
hur_his = xr.load_dataset(f'{data_transfer}/{hur_his_fname}')
hur_370 = xr.load_dataset(f'{data_transfer}/{hur_370_fname}')
# tas_his = gl.load_var(
#     var='tas',experiment_id='historical', member_id=member_id, years=years_his)
# tas_585 = gl.load_var(
#     var='tas',experiment_id='ssp585', member_id=member_id, years=years_585)

#%% load obs
f_tmax = xr.open_dataset(path_to_data +
    f"tmax.e5.daily.highres.{start}-{end-1}.nc")
f_tmin = xr.open_dataset(path_to_data + 
    f"tmin.e5.daily.highres.{start}-{end-1}.nc")

tas_obs = (f_tmax.t2m + f_tmin.t2m) / 2

#%%
# regrid obs to CESM grid
regridder = xe.Regridder(tas_obs, tas_his, "bilinear")
tas_obs_coarse = regridder(tas_obs)
pr_obs_coarse = regridder(tas_obs)
hur_obs_coarse = regridder(tas_obs)

#%%
# do dbcca on tas

DBCCA(tas_his,tas_585,tas_obs_coarse,tas_obs,n_analogues=30,
    window_size=45, window_unit='days', write_output=True, do_future=True
    fout_hist_bcca=tas_his_bcca_file, fout_future_bcca=tas_585_bcca_file,
    fout_hist_dbcca=tas_his_dbcca_file, fout_future_dbcca=tas_585_dbcca_file)

#%%
pr_dbcca_file = f'pr_dbcca.nc'
DBCCA(pr_his,pr_obs_coarse,pr_obs,n_analogues=30,
    window_size=45, window_unit='days', fout=f'{path_to_data}/pr_dbcca_file')
# pr = gl.load_var(
#     var='pr',experiment_id='historical', years=years_hist)
# hur = gl.load_var(
#     var='hur',experiment_id='historical', years=years_hist)
#%%
# pr_masked = gl.mask_region(
#     pr,x_dim='lon',y_dim='lat',shapefile_name=f"{path_to_data}/Gezira.shp")

#%%
# test
tas_his_mean = tas_his.mean(dim=['lat','lon'])
tas_his_mean = tas_his_mean.groupby('time.dayofyear').mean(dim='time')
tas_obs_mean = tas_obs.mean(dim=['lat','lon'])
tas_obs_mean = tas_obs_mean.groupby('time.dayofyear').mean(dim='time')
#%%
plt.plot(tas_his_mean.dayofyear, tas_his_mean)
# plt.plot(tas_obs_mean.dayofyear, tas_obs_mean)