import os
from helper_funcs import get_model_year_file, models, variables, scen
from cdo import Cdo
from pathlib import Path
from multiprocessing import Pool
cdo = Cdo()


OUTDIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/EnsMean')

def get_ensemble_files(year, models: list, variable, scen):
	files = {model : get_model_year_file(year, model, variable, scen)[0]
			for model in models}

	return files


# TODO: Change to include ens_id in the outfile name
# Plus what about the existing files? Damnit ==> Rename?
def get_outfile_name(year, model, variable, scen):

	outname = '_'.join([variable, 'day', model, scen, f'{year}.nc'])

	return outname


def make_ensemble_mean(year, models, variable, scen, outdir):
	ens_files = list(get_ensemble_files(year, models, variable, scen).values())
	cmd = ' '.join(ens_files)

	outname = get_outfile_name(year, 'EnsMean', variable, scen)
	outfile = f"{outdir}/{variable}/{outname}"
	os.system(f'mkdir -p {outdir}/{variable}')
	cdo.ensmean(input=cmd, output=outfile)



years = {'historical': range(1950, 2006),
		 'rcp45': range(2005, 2099),
		 'rcp85': range(2005, 2099)}

pool = Pool()

for year in years['historical']:
	pool.apply_async(make_ensemble_mean, [year, models, 
									   'pr', 'historical', 
									   f'{OUTDIR}/ALL21_yearwise'])


pool.close()
pool.join()


