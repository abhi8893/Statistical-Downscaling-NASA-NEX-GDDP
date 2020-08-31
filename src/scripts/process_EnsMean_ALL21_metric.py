from Model import *

variables = ['pr', 'tasmax', 'tasmin', 'tas']
scens = ['historical', 'rcp45', 'rcp85']
tslices = ['2021-2050', '2061-2090']
base_year = '1976-2005'

outdir = '/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED'

for model in ['EnsMean_ALL21']:
	for variable in variables:
		for scen in scens:
			m = NEXModel.from_details(model=model, variable=variable, scen=scen)
			m.outdir = outdir
			# m.process('monmin', outdir='auto', outname='auto')
			# m.process('monmax', outdir='auto', outname='auto')

			if scen == 'historical':
				m.process('ydaymin', year_str=base_year, outdir='auto', outname='auto')
				m.process('ydaymax', year_str=base_year, outdir='auto', outname='auto')
				m.process('ydaymean', year_str=base_year, outdir='auto', outname='auto')

			else:
				for tslice in tslices:
					m.process('ydaymin', year_str=tslice, outdir='auto', outname='auto')
					m.process('ydaymax', year_str=tslice, outdir='auto', outname='auto')
					m.process('ydaymean', year_str=tslice, outdir='auto', outname='auto')

