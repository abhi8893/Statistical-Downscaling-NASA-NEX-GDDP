from Model import *

variables = ['pr', 'tasmax', 'tasmin']
scens = ['historical', 'rcp45', 'rcp85']
tslices = ['2021-2050', '2061-2090']
base_year = '1976-2005'
seasons = ['Annual', 'JJAS', 'ON', 'DJF', 'MAM']

outdir = '/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED'

for model in models[1:]:
	for variable in variables:
		for scen in scens:
			m1 = NEXModel.from_details(model=model, variable=variable, scen=scen)
			m1.outdir = outdir

			for stat in ['mean', 'max', 'min']:
				if scen == 'historical':
					m2 = [NEXModel(f=m1.retrieve(metric=f'yday{stat}', year_str=base_year),
								   outdir=outdir)]
				else:
					m2 = [NEXModel(f=m1.retrieve(metric=f'yday{stat}', year_str=tslice),
								   outdir=outdir)
						  for tslice in tslices]

				for m in m2:
					for seas in seasons:
						m.process(metric=f'tim{stat}', seas=seas, outdir='auto', outname='auto')
			