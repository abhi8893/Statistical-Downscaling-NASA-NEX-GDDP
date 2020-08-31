from cdo import Cdo
cdo = Cdo()
import glob

import sys
sys.path.append('../scripts/')
from Model import *
from multiprocessing import Pool

seasons = ['Annual', 'JJAS', 'ON', 'DJF', 'MAM']

DATA_DIR = '/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT'


def get_region_year_files(model, variable, scen, region='Amravati'):
    if 'EnsMean' in model:
        dir1, dir2 = model.split('_')
        model = 'EnsMean'
    else:
        if model in ['BCC-CSM1-1', 'INMCM4']:
            model = model.lower()
            
        dir1, dir2 = 'Models', model
    
    p = f'{DATA_DIR}/region-wise/{region}/year-wise/{dir1}/{dir2}/{variable}/'
    p += f'{variable}*{scen}*'
    files = glob.glob(p)
    files_year = list(map(lambda x: x.split('_')[-1], files))
    sorted_files = [f for _, f in sorted(zip(files_year, files))]
    
    return(sorted_files)



if __name__ == '__main__':

	def Process(m, kwargs):
		m.process(**kwargs)




	pool = Pool()
	for model in models:
		for variable in ['pr', 'tasmax']:
			for scen_name in scen:
				files = get_region_year_files(model, variable, scen_name)
				for f in files:
					m = NEXModel(f)
					m.outdir = '/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED/region-wise/Amravati/year-wise'


					for seas in seasons:
						if variable == 'pr':
							index_kwargs = {'thresh': 1, 'ndays': 5}
							for index in ['cdd', 'cwd']:
								kwargs = dict(metric=index, index_kwargs=index_kwargs, 
											  seas=seas, op_chain=['-mulc,86400'], outdir='auto', outname='auto')
								pool.apply_async(Process, [m, kwargs])
								# m.process(index, index_kwargs=index_kwargs, year_str=tslice, seas=seas,
								# 		  outdir='auto', outname='auto')

						elif variable == 'tasmax':
							for thresh in [30, 35, 40]:
								for ndays in [3, 5, 7]:
									index_kwargs = {'thresh': thresh, 'ndays': ndays}
									kwargs = dict(metric='chd', index_kwargs=index_kwargs, 
												  seas=seas, op_chain=['-subc,273.15'], outdir='auto', outname='auto')
									pool.apply_async(Process, [m, kwargs])
									# m.process('chd', index_kwargs=index_kwargs, year_str=tslice, seas=seas,
									# 		   outdir='auto', outname='auto')



	pool.close()
	pool.join()


