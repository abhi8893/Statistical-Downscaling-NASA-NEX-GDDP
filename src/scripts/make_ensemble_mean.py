import os
from cdo import Cdo
from pathlib import Path
from helper_funcs import get_model_year_combined_file, models, variables, scen
from tqdm import tqdm
import time

cdo = Cdo()

OUTDIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/EnsMean')


def get_ensemble_files(models: list, variable, scen):
	files = {model : get_model_year_combined_file(model, variable, scen) 
			 for model in models}

	return files

def get_outfile_name(model, variable, scen):
	if scen == 'historical':
		year_str = '1950-2005.nc'
	else:
		year_str = '2006-2099.nc'


	outname = '_'.join([variable, 'day', model, scen, year_str])

	return outname


def make_ensemble_mean(models, variable, scen, outdir):
	ens_files = list(get_ensemble_files(models, variable, scen).values())
	cmd = ' '.join(ens_files)

	outname = get_outfile_name('EnsMean', variable, scen)
	outfile = f"{outdir}/{variable}/{outname}"
	os.system(f'mkdir -p {outdir}/{variable}')
	cdo.ensmean(input=cmd, output=outfile)



# for variable in tqdm(variables):
# 	for scen_name in tqdm(scen):
# 		make_ensemble_mean(models, variable, scen_name, f'{OUTDIR}/ALL21')