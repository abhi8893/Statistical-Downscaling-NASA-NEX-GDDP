from Model import *

variables = ['tas', 'tasmax', 'tasmin']
base_year = '1976-2005'
tslices = ['2021-2050', '2061-2090']
scens = ['historical', 'rcp45', 'rcp85']
outdir = '/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED'

for variable in variables:
	for scen in scens:
		m = NEXModel.from_details(model='EnsMean_ALL21', variable=variable, scen=scen)
		m.outdir = outdir
		if scen == 'historical':
			m.process('monmean', year_str=base_year, outdir='auto', outname='auto')
		else:
			for tslice in tslices:
				m.process('monmean', year_str=tslice, outdir='auto', outname='auto')

