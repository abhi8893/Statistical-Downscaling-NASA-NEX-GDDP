from Model import *

variables = ['pr', 'tasmax', 'tasmin']
scens = ['historical', 'rcp45', 'rcp85']
tslices = ['2021-2050', '2061-2090']
base_year = '1976-2005'
seasons = ['Annual', 'JJAS', 'ON', 'DJF', 'MAM']

outdir = '/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED'

def get_minmax_dict(m, method, year_str, **kwargs):
	minmax_dict = {stat: m.retrieve(metric=f'{method}{stat}', year_str=year_str, **kwargs)
				   for stat in ['min', 'max']}

	return(minmax_dict)



for model in models[15:]:
	for variable in variables:
		for scen in scens:
			m = NEXModel.from_details(model=model, variable=variable, scen=scen)
			m.outdir = outdir

			for method in ['tim', 'yday']:
				if method == 'tim':
					seas_to_calc = seasons
				else:
					seas_to_calc = ['Annual']


				for seas in seas_to_calc:
					if scen == 'historical':
						minmax_dicts = {base_year: get_minmax_dict(m, method=method, year_str=base_year, seas=seas)}
					else:
						minmax_dicts = {tslice: get_minmax_dict(m, method=method, year_str=tslice, seas=seas)
										for tslice in tslices}


					for year_str, minmax_dict in minmax_dicts.items():
						for pctl in [5, 10, 25, 50, 75, 90, 95, 99]:
							m.process(metric='percentile', method=method, pctl=pctl, seas=seas,
									  year_str=year_str, depends=minmax_dict, 
									  outdir='auto', outname='auto')


