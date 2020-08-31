from cdo import Cdo
import xarray as xr
import os
import sys
from pathlib import Path
import glob
import difflib
from collections import OrderedDict
import re
import pandas as pd
from tqdm import tqdm
from nco import Nco
from multiprocessing import Pool

cdo = Cdo()

DATA_DIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA')
OUT_DIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT')
os.system(f'mkdir -p "{OUT_DIR}"')

models =   [dI for dI in os.listdir(DATA_DIR) 
if os.path.isdir(os.path.join(DATA_DIR,dI))]

variables = ['pr', 'tasmax', 'tasmin']
scen = ['historical', 'rcp45', 'rcp85']

possibilities = OrderedDict({'model': models,
 'variable': variables,
 'scen': scen})

def get_apt_names(model, variable, scen):
	model, variable, scen = [difflib.get_close_matches(word, possible, n=1, cutoff=0)[0]
				for word, possible in zip([model, variable, scen], possibilities.values())]
	
	return [model, variable, scen]

def get_model_files(model, variable, scen, model_data_dir=DATA_DIR):
	# model, variable, scen = get_apt_names(model, variable, scen)
	
	return glob.glob(f'{model_data_dir}/{model}/{variable}/*{scen}*.nc')

def make_year_combined_file(model, variable, scen, model_data_dir=DATA_DIR, outdir=None):
	
	model, variable, scen = get_apt_names(model, variable, scen)

	model_files = get_model_files(model, variable, scen, model_data_dir=model_data_dir)
			
	# Make outdir
	if (outdir is None):
		outdir = f'{OUT_DIR}/model_year_combined/{model}/{variable}'

	os.system(f'mkdir -p {outdir}')
	any_file = model_files[0]
	# ens_id =  Path(any_file).name.split('_')[-2]

		
	cmd = ' '.join(model_files)
		
		
	if scen == 'historical':
	  year_str = '1950-2005.nc'
	else:
	  year_str = '2006-2099.nc'
			  
		  
	outname = '_'.join([variable, 'day', model, scen, year_str])
	outfile = f"{outdir}/{outname}"

	cdo.mergetime(input=cmd,
			output=f"{outdir}/tmp.nc",
			env={"SKIP_SAME_TIME": "1"})
		
	if variable == "pr":
		cdo.mulc('86400', input=f"-setunit,mm/day {outdir}/tmp.nc",
			output=outfile)
		
	elif variable in ['tasmax', 'tasmin']:
		cdo.addc('-273.15', input=f"-setunit,C {outdir}/tmp.nc",
			output=outfile)        
		
	os.system(f'rm {outdir}/tmp.nc')
		
	
		
	return(outfile)

# dont_merge = pd.read_csv('pickles/check_file_status/dont_merge.csv')

# def is_OK(model, variable, scen):
# 	return(dont_merge.loc[((dont_merge.model == model) & 
# 		(dont_merge.variable == variable) &
# 		(dont_merge.scen == scen))].empty)
	
	

# pbar = tqdm(possibilities['model'])
# for model in pbar:
# 	for variable in possibilities['variable']:
# 		for scen in possibilities['scen']:

# 			if not is_OK(model, variable, scen):
# 				pbar.set_description(f'Processing {model}, {variable}, {scen}')
# 				make_year_combined_file(model, variable, scen)
				
# 				#pool = Pool(8)
				#pool.apply_async(make_year_combined_file, [model, variable, scen])
				#pool.close()
				#pool.join()
				
				
				

									


