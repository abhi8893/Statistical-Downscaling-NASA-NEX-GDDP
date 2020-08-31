from Model import *

variables = ['pr', 'tas', 'tasmax', 'tasmin']
base_year = '1976-2005'
outdir = '/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED'

data_dir = '/home/abhi/Documents/data/OBSERVATION/IMD'
obs_data = {'pr': f'{data_dir}/precip/IMD_pr_1901-2017.nc',
			'tas': f'{data_dir}/tmean/IMD_MeanT_1969-2016.nc',
			'tasmax': f'{data_dir}/tmax/IMD_MaxT_1969-2005.nc',
			'tasmin': f'{data_dir}/tmin/IMD_MinT_1969_2005.nc'}

for variable in variables[0:1]:
	m = NEXModel(f=obs_data[variable],
				 parse_details=False,
				 model='IMD',
				 variable=variable,
				 scen='observation',
				 model_type='Observation')

	m.outdir = outdir

	m.process('monmean', year_str=base_year, outdir='auto', outname='auto')


