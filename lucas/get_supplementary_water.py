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
path_to_downscaled = 'C:/Users/prate/Desktop/Climate Impacts Hackathon/data/downscaled/'

forcing = 'his' # or '370'
bias_correction='dbcca' # or 'bcca'
f_precip = xr.open_dataset(path_to_downscaled+f"pr.{forcing}.{bias_correction}.nc")
f_rhumid = xr.open_dataset(path_to_downscaled+f"hur.{forcing}.{bias_correction}.nc")
f_temp = xr.open_dataset(path_to_downscaled+f"tas.{forcing}.{bias_correction}.nc")
                         
precip_mod=mask_region_cesm(f_precip.pr) * 3600 * 24
precip_mod=precip_mod.mean(dim=('lat','lon'))

rhumid_mod=mask_region_cesm(f_rhumid.hur) * 100
rhumid_mod=rhumid_mod.mean(dim=('lat','lon'))

temp_mod=mask_region_cesm(f_temp.tas)
temp_mod=temp_mod.mean(dim=('lat','lon'))

revap_mod=reference_crop_evapotranspiration(temp_mod,rhumid_mod)
