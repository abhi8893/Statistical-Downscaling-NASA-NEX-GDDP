from helper_funcs import get_EnsMean_year_files, scen_year_str
from cdo import Cdo
from tqdm import tqdm
from pathlib import Path
import os
import glob
from multiprocessing import Pool


cdo = Cdo()

OUTDIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/EnsMean')
REGION_DIR = '/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/region-wise'


def get_region_EnsMean_year_files(variable, scen, Ens_type, region='Amravati'):
	files_dir = f'{REGION_DIR}/{region}/year-wise/EnsMean/{Ens_type}/{variable}'
	files = glob.glob(f'{files_dir}/{variable}*{scen}*')
	files_year = list(map(lambda x: x.split('_')[-1], files))
	sorted_files = [f for _, f in sorted(zip(files_year, files))]

	return(sorted_files)



def make_EnsMean(variable, scen, Ens_type='ALL21', region='Amravati', outdir=None):
	ens_files = get_region_EnsMean_year_files(variable, scen, Ens_type, 
											  region=region)
	if outdir is None:
		outdir = f'{OUTDIR}/{Ens_type}'

	os.system(f'mkdir -p {outdir}/{variable}')

	if variable == 'pr':
		op = eval('cdo.mulc')
		arg = '86400'
	elif variable in ['tasmax', 'tasmin', 'tas']:
		op = eval('cdo.addc')
		arg = '-273.15'

	# ens_files = list(map(lambda f: f'-{op},{arg} {f}', ens_files))

	outname = '_'.join([variable, 'day', 'EnsMean', 
					    scen, scen_year_str[scen]])

	outfile = f'{outdir}/{variable}/{outname}.nc'

	ens_files = ' '.join(ens_files)

	op(arg, input=f'-mergetime {ens_files}', output=outfile, 
				  env={'SKIP_SAME_TIME': '1'})



if __name__ == '__main__':
	region_outdir = f'{REGION_DIR}/Amravati/merged/EnsMean/ALL21'

	variables = ['pr', 'tasmax', 'tasmin']
	scens = ['historical', 'rcp45', 'rcp85']

	pool = Pool()

	for variable in variables:
		for scen in scens:

			pool.apply_async(make_EnsMean, (variable, scen, 'ALL21',
							 'Amravati', region_outdir))


	pool.close()
	pool.join()

	# for variable in tqdm(variables):
	# 	for scen_name in tq