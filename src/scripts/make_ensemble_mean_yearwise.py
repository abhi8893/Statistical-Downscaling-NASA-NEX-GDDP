import os
from cdo import Cdo
from pathlib import Path
from helper_funcs import get_model_year_file, scen_year_str
from helper_funcs import models, variables, scen
from tqdm import tqdm
import time
from multiprocessing import Pool


cdo = Cdo()

OUTDIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/EnsMean_yearwise')
DATA_DIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA')

model_data_dir = '/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/region-wise/Amravati/year-wise/Models'


def get_ensemble_files(year, models: list, variable, scen, model_data_dir=DATA_DIR):
	files = \
			 {model : get_model_year_file(year, model, variable, scen, 
									 	  model_data_dir=model_data_dir) 
				 for model in models}
			
	return files

def get_outfile_name(year, model, variable, scen):

	outname = '_'.join([variable, 'day', model, scen, f'{year}.nc'])

	return outname


def make_ensemble_mean(year, models: list, variable, scen, outdir):

	ens_files = list(get_ensemble_files(year, models, variable, scen).values())
	cmd = ' '.join(ens_files)
	year_ens_merged = cdo.mergetime(input=cmd)

	outname = get_outfile_name(year, 'EnsMean', variable, scen)
	outfile = f"{outdir}/{variable}/{outname}"
	os.system(f'mkdir -p {outdir}/{variable}')
	cdo.daymean(input=year_ens_merged, output=outfile)

	os.system(f'rm {year_ens_merged}')



if __name__ == '__main__':


	for variable in tqdm(variables):
		for scen_name in tqdm(scen):
			years = scen_year_str[scen_name].split('-')
			y1 = int(years[0])
			y2 = int(years[1])

			# outdir = f'{OUTDIR}/ALL21'


			for year in tqdm(range(y1, y2+1)):
				make_ensemble_mean(year, models, variable, scen_name, outdir)

