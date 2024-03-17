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
f_rhumid = xr.open_dataset(path_to_mod+f"RH.cesm.daily.historical.nc")
f_temp = xr.open_dataset(path_to_mod+f"tas.cesm.daily.historical..nc")