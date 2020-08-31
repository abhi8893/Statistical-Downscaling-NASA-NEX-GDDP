from helper_funcs import possibilities


from tqdm import tqdm
import time

pbar_m = tqdm(possibilities['model'])
for model in pbar_m:
	pbar_m.set_description(model)
	pbar_v = tqdm(possibilities['variable'])
	for variable in pbar_v:
		pbar_v.set_description(variable)
		pbar_s = tqdm(possibilities['scen'])
		for scen in pbar_s:

			pbar_s.set_description(scen)
			time.sleep(0.1)
