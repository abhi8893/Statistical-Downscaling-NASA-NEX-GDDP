from make_ensemble_mean_yearwise import *

	for variable in tqdm(variables):
		for scen_name in tqdm(scen):
			years = scen_year_str[scen_name].split('-')
			y1 = int(years[0])
			y2 = int(years[1])

			outdir = f'{OUTDIR}/ALL21'

			for year in tqdm(range(y1, y2+1)):
				make_ensemble_mean(year, models, variable, scen_name, outdir)