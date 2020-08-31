from cdo import Cdo
cdo = Cdo()
import glob

import sys
sys.path.append('../scripts/')
from Model import *
from multiprocessing import Pool

seasons = ['Annual', 'JJAS', 'ON', 'DJF', 'MAM']


def get_dirs(model):
    if re.match(re.compile('EnsMean_.*'), model):                          
        dir_1, dir_2 = model.split('_')
    else:
        dir_1, dir_2 = ['Models', model]

    return [dir_1, dir_2]

def get_data_dir(model, region='Amravati'):
    dir_1, dir_2 = get_dirs(model)
        
    data_dir = f'/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/region-wise/{region}/merged/{dir_1}/{dir_2}'
        
    return data_dir

def get_model_year_combined_file(model, variable, scen, region='Amravati'):

    data_dir = get_data_dir(model, region=region)
    return glob.glob(f'{data_dir}/{variable}/*{scen}*')[0]



if __name__ == '__main__':

	def Process(m, kwargs):
		m.process(**kwargs)


	pool = Pool()
	for model in models[1:]:
		for variable in ['pr', 'tasmax']:
			for scen_name in scen:
				f = get_model_year_combined_file(model, variable, scen_name)
				m = NEXModel(f)
				m.outdir = '/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED/region-wise/Amravati/merged'

				if scen_name == 'historical':
					tslices = ['1976-2005']
				else:
					tslices = ['2021-2050', '2061-2090']



				for tslice in tslices:
					for seas in seasons:
						if variable == 'pr':
							index_kwargs = {'thresh': 1, 'ndays': 5}
							for index in ['cdd', 'cwd']:
								kwargs = dict(metric=index, index_kwargs=index_kwargs, year_str=tslice, 
											  seas=seas, outdir='auto', outname='auto')
								pool.apply_async(Process, [m, kwargs])
								# m.process(index, index_kwargs=index_kwargs, year_str=tslice, seas=seas,
								# 		  outdir='auto', outname='auto')

						elif variable == 'tasmax':
							for thresh in [30, 35, 40]:
								for ndays in [3, 5, 7]:
									index_kwargs = {'thresh': thresh, 'ndays': ndays}
									kwargs = dict(metric='chd', index_kwargs=index_kwargs, year_str=tslice, 
												  seas=seas, outdir='auto', outname='auto')
									pool.apply_async(Process, [m, kwargs])
									# m.process('chd', index_kwargs=index_kwargs, year_str=tslice, seas=seas,
									# 		   outdir='auto', outname='auto')



	pool.close()
	pool.join()


