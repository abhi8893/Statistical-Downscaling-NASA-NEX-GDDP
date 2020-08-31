from Model import *

variables = ['pr', 'tasmax', 'tasmin']
scens = ['historical', 'rcp45', 'rcp85']
outdir = '/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED'

for model in models:
	for variable in variables:
		for scen in scens:
			m = NEXModel.from_details(model=model, variable=variable, scen=scen)
			m.outdir = outdir
			m.process('monmean', outdir='auto', outname='auto')
