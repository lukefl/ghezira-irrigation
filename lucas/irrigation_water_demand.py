import numpy as np
from cftime import num2pydate

# names of crops
SORGHUM='sorghum'
WHEAT='wheat'
GROUNDNUTS='groundnuts'
COTTON='cotton'

# crop coefficients. fill value = -1
KC = {}
KC[SORGHUM]=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0.39,0.95,1.10,0.81,1.96,np.nan]
KC[WHEAT]=[1.15,1.04,0.43,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,0.23,0.75]
KC[GROUNDNUTS]=[np.nan,np.nan,np.nan,np.nan,0.42,0.96,1.44,1.08,1.00,np.nan,-np.nan,np.nan]
KC[COTTON]=[np.nan,np.nan,0.35,0.63,0.91,1.20,1.20,1.00,0.80,0.60,np.nan,np.nan]

def reference_crop_evapotranspiration(temp, rh):
    return 16 * temp / rh
    
def crop_water_demand(crop, temp, rh, time):
    """
    Return the total water demand for a given crop,
    temperature (temp), and relative humidity (rh) during 
    a given day of the year
    """
    mon_index = time.dt.month - 1
    #mon_index = num2pydate(day, f'days since {year}-01-01 00:00:00', calendar='proleptic_gregorian').month - 1
    return KC[crop][mon_index] * reference_crop_evapotranspiration(temp, rh)

def irrigation_water_demand(crop, temp, rh, time, er, eff):
    """
    Returns the amount of water required from supplementary
    sources for irrigation of a given crop, at temperature temp,
    relative humidity rh, effective rainfall er, and irrigation 
    efficiency eff
    """
    return (crop_water_demand(crop, temp, rh, time) - er) / eff


if __name__ == '__main__':
    mon_index = num2pydate([1, 31], f'days since 1980-01-01 00:00:00', calendar='proleptic_gregorian').month - 1
    print(KC[SORGHUM][mon_index])