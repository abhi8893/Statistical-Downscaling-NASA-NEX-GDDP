import sys
sys.path.append("/home/abhi/Documents/mygit/postBC_diagnostic/src/scripts")
from recipes import *
import re


def groupby(ds, method='whole'):
    if method == 'whole':
        ds = ds
    elif method == 'month':
        ds = ds.groupby('time.month')
    elif method == 'doy':
        ds = ds.groupby('time.dayofyear')
    elif method == 'seas':
        ds = groupbyseas(ds)
        
    return(ds)


def calc_pctl(ds, q, method='whole'):
    ds = groupby(ds, method=method)
    res = ds.reduce(np.percentile, q=q, dim='time')
        
    return(res)



def make_seas_q(ds, pctl):
	qseas = calc_pctl(ds, pctl, method='seas')
	qwhole = calc_pctl(ds, pctl, method='whole')

	q = xr.concat([qwhole] + [qseas.sel(seas=seas).drop('seas') for seas in seasIndex[1:]],
				  dim=seasIndex)

	return(q)


def get_thresh_val_from_str(thresh):
	p = re.compile(r'([\-]?[0-9]+[\.[0-9]?[0-9]?]?).')
	thresh_val = float(p.search(thresh).groups()[0])

	return(thresh_val)



def change_units(ds, to='mm/day', copy=True):
    if copy:
        ds = ds.copy()
        
    ds.attrs['units'] = to
    return(ds)


