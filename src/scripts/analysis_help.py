# Need an outfile namer
#  -must be as descriptive as possible [long]
# Metrics to consider

from helper_funcs import get_data_dir, models, variables, scen
import re
from copy import deepcopy
from collections import OrderedDict
from cdo import Cdo
from pathlib import Path

cdo = Cdo()


default = {}

default['units'] = {'pr': 'mm',
					'tas': 'C',
					'tasmax': 'C',
					'tasmin': 'C'}

default['years'] = {'historical': '1950-2005',
	                'rcp45': '2006-2099',
	                'rcp85': '2006-2099'}










# default['time_slice'] = {'historical': '1950-2005',
		 #                 'rcp45': '2006-2099',
		 #                 'rcp85': '2006-2099'}
default_kwargs = OrderedDict({'seas': 'Annual',
							  'year_str': None,
							  'thresh': None,
							  'thresh_type': 'gtc'})



def get_kwargs(kwargs, return_keys):

	default_kwargs = OrderedDict({'seas': 'Annual',
								  'thresh': None,
								  'thresh_type': 'gtc'})

	default_kwargs.update(kwargs)

	return [default_kwargs[k] for k in return_keys]







# NOTE: specify thresh as 1mm | 40C
def percentile_str(pctl, method='tim', **kwargs):

	seas, thresh, thresh_type = get_kwargs(kwargs, 
										   ['seas', 'thresh', 'thresh_type'])


	name = '-'.join([f'{method}pctl{pctl}p', 
				     thresh_str(thresh, thresh_type),
					 seas_str(seas)])

	return name


def thresh_str(thresh, thresh_type=default_kwargs['thresh_type']):

	if thresh is not None:
		return f'{thresh_type}{thresh}'
	else:
		return ''


def seas_str(seas=default_kwargs['seas']):
	return f'{seas}'




# R-style if missing(arg) so that I don't have to keep thresh at the end?
def percentile_outname(model, variable, scen, year_str, 
					   pctl, method='tim', thresh=None):                       

	outname_prefix = f'{variable}'
	outname_metric_str = percentile_str(pctl, method, thresh=thresh)
	outname_suffix = f'{model}_{scen}_{year_str}'

	outname = '_'.join([outname_prefix, outname_metric_str, outname_suffix])

	return outname



# Depends on: min and max files
def percentile_cmd(file, pctl, method='tim', 
			       minmax_files=None,
			       op_chain=None, **kwargs):

	file = apply_kwargs(file, kwargs)
	file = apply_op_chain(file, op_chain) if op_chain is not None else file

	cmd = f'-{method}pctl,{pctl} {file} '

	if minmax_files is None:
		minfile, maxfile = file, file

	else:
		minfile, maxfile = minmax_files['min'], minmax_files['max']

	cmd += f'-{method}min {minfile} '
	cmd += f'-{method}max {maxfile}'

	return cmd



def process(cmd, output=None):


	# Refactor: This is too messy.
	p = re.compile(r'^[^\s]+')
	last_op_arg = p.findall(cmd)[0].split(',')
	op = last_op_arg[0]
	op = op[1:] if op.startswith('-') else op
	op = f'cdo.{op}'
	op = eval(op)

	try:
		arg = last_op_arg[1]
	except IndexError:
		arg = None


	if arg is not None:
		input_str = p.sub('', cmd, 1).strip()
		output = op(arg, input=input_str, output=output)


	return output




def get_threshval(thresh):

	if thresh is not None:
		p = re.compile(r'^\d+')
		thresh = float(p.findall(thresh)[0])

	return thresh


def apply_kwargs(file, kwargs, **func_kwargs):

	global default_kwargs
	default_kwargs = deepcopy(default_kwargs)
	default_kwargs.update(kwargs)

	seas, year_str, thresh, thresh_type = [default_kwargs[p] 
							     for p in ['seas', 'year_str',
									       'thresh', 'thresh_type']]

	thresh_val = get_threshval(thresh)

	file = f'-selseas,{seas} {file}' if seas != 'Annual' else file

	if year_str is not None:
		y1, y2 = year_str.split('-')
		file = f'-selyear,{y1}/{y2} {file}'

	thresh_kwargs = func_kwargs.get('thresh', {})

	file = apply_thresh_op(file, thresh, thresh_type, **thresh_kwargs) \
		   if thresh is not None else file

	return file

def apply_thresh_op(file, thresh, thresh_type, 
	set_miss_range_to='missval'):
	thresh_val = get_threshval(thresh)

	if thresh_type == 'gtc':
		miss_range = f'-inf,{thresh_val}'

	elif thresh_type == 'ltc':
		miss_range = f'{thresh_val},inf'

	if set_miss_range_to == 'missval':
		op = f'-setrtomiss,{miss_range}'
	else:
		op = f'-setrtoc,{miss_range},{set_miss_range_to}'

	return f'{op} {file}'


def apply_op_chain(file, op_chain):

	if op_chain is None:
		return file
	else:
		op_chain = [f'-{op}' if not op.startswith('-') else op 
					for op in op_chain]


		file_op = ' '.join(op_chain) + ' ' + file

	return file_op





		
if __name__ == '__main__':

	from helper_funcs import models, get_model_year_combined_file

	model = models[0]
	scen_name = 'rcp45'
	variable = 'pr'
	f = get_model_year_combined_file(model, variable, scen_name)
	cmd = percentile_cmd(f, 90)







# {'time-pctl': {'clim' : ['*p', '*pthresh*'],
# 				'yday': ['*p', '*pthresh*']}}