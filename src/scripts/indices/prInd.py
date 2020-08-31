import xclim as xc
import xarray as xr
import _pickle as cpickle
import numpy as np
import re
from utils import *

import sys
sys.path.append("/home/abhi/Documents/mygit/postBC_diagnostic/src/scripts")
from recipes import *

seasIndex = pd.Index(['Annual', 'DJF', 'MAM', 'JJAS', 'ON'], name='seas')

def intensity_above_thresh(ds, thresh='1 mm/day', freq='MS'):
    res = yearseasmean(xc.indices.daily_pr_intensity(ds, thresh=thresh, freq='MS'))
    return(res)


def days_above_thresh(ds, thresh='1 mm/day', freq='MS'):
    res = yearseassum(xc.indices.wetdays(ds, thresh=thresh, freq='MS'))
    return(res)


def days_above_pctl(ds_fut, ds_base, pctl=90):

	q = make_seas_q(ds_base, pctl)

	res = []

	for seas in seasIndex:
		if 'model' in ds_fut.coords:
		    anom  = selseas(ds_fut, seas).groupby('model') - q.sel(seas=seas)
		else:
		    anom  = selseas(ds_fut, seas) - q.sel(seas=seas)

		anom.attrs['units'] = 'mm/day'
	    
		res.append(xc.indices.wetdays(anom, '0 mm/day', freq='YS'))
	    

	res = xr.concat(res, dim=seasIndex)


	return(res)


def intensity_above_pctl(ds_fut, ds_base, pctl=90):

	q = make_seas_q(ds_base, pctl)

	res = []

	for seas in seasIndex:
		if 'model' in ds_fut.coords:
		    anom  = selseas(ds_fut, seas).groupby('model') - q.sel(seas=seas)
		else:
		    anom  = selseas(ds_fut, seas) - q.sel(seas=seas)

		anom.attrs['units'] = 'mm/day'
	    
		res.append(ds_fut.where(anom > 0).resample(time='YS').mean())
	    

	res = xr.concat(res, dim=seasIndex)


	return(res)


def max_n_day_pr_amt(ds, ndays=5, **kwargs):
	results = {}

	for seas in seasIndex:
	    results[seas] = (xc.indices
				         .max_n_day_precipitation_amount(selseas(ds, seas),
	                                                     window=ndays, **kwargs)
				         )
	    
	res = xr.concat(results.values(), dim=seasIndex)

	return(res)



def max_consec_days(ds, metric, thresh='1 mm/day', **kwargs):
    
	if metric == 'cdd':
	    func = xc.indices.maximum_consecutive_dry_days
	elif metric == 'cwd':
	    func = xc.indices.maximum_consecutive_wet_days
	    

	results = {}

	for seas in seasIndex:
	    results[seas] = func(selseas(ds, seas), thresh=thresh, **kwargs)
	    
	res = xr.concat(results.values(), dim=seasIndex)

	return(res)


def num_consec_days(ds, metric, thresh='1 mm/day', ndays=5):
	thresh_val = get_thresh_val_from_str(thresh)

	if metric == 'cdd':
	    cond = ds < thresh_val
	elif metric == 'cwd':
	    cond = ds > thresh_val
	    
	results = {}

	for seas in seasIndex:
	    results[seas] = (selseas(cond, seas)
	                     .groupby('time.year')
	                     .apply(xc.run_length.windowed_run_count, window=ndays)
	                    )
	    

	res = xr.concat(results.values(), dim=seasIndex)

	return(res)

    