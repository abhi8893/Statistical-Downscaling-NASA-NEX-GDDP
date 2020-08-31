from make_merged_year_files import make_year_combined_file
from helper_funcs import possibilities
from tqdm import tqdm

model_data_dir = '/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/region-wise/Amravati/year-wise/Models'

pbar_m = tqdm(possibilities['model'])
for model in pbar_m:
	pbar_m.set_description(model)
	pbar_v = tqdm(possibilities['variable'])
	for variable in pbar_v:
		pbar_v.set_description(variable)
		pbar_s = tqdm(possibilities['scen'])
		for scen in pbar_s:

			pbar_s.set_description(scen)

			outdir = f'/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/region-wise/Amravati/merged/{model}/{variable}'

			make_year_combined_file(model, variable, scen, 
									model_data_dir=model_data_dir, 
									outdir=outdir)