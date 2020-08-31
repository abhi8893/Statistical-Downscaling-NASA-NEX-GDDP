from Metric import Metric
from helper_funcs import models, variables, scen
from helper_funcs import get_model_year_combined_file
from pathlib import Path
import re
import warnings
import os
from copy import deepcopy

variables = ['pr', 'tas', 'tasmax', 'tasmin']


class NEXModel(Metric):

	def __init__(self, f, parse_details=True, **kwargs):


		# TODO: Subclass pathlib.Path
		self.path = Path(f)
		self.file = f
		self.name = self.path.name

		if parse_details:
			self.__dict__.update(self.parse(self.file))

		self.__dict__.update(kwargs)


		super().__init__(**kwargs)


	@classmethod
	def from_details(cls, model, variable, scen, 
					 parse_details=True, **kwargs):
		f = get_model_year_combined_file(model, variable, scen)
		return cls(f, parse_details, **kwargs)


	def __sub__(self, other):
		res = deepcopy(self)
		res.compare_obj = deepcopy(other)
		return res






	@staticmethod		
	def parse(f):
		global models, variables, scen

		fname = Path(f).name

		grp = dict()

		for grp_name, grp_lst in zip(['model', 'variable', 'scen'],
			[models+['EnsMean'], variables, scen]): # FIX Model group!
		                                                  # to include EnsMean_*

			grp[grp_name] = '|'.join(grp_lst)

		# Refactor!

		p_str = f"({grp['variable']})" # variable
		p_str += "_"
		p_str += "(.*)" # metric_str
		p_str += "_"
		p_str += f"({grp['model']})" # model
		p_str += "_"
		p_str += f"({grp['scen']})" # scen
		p_str += "_"
		p_str += "(.*)\.nc" # year_str

		p = re.compile(p_str, re.IGNORECASE)

		grp_names = ['variable', 'metric_str', 'model', 'scen', 'year_str']
		matches_grps = p.search(fname).groups()
		attr_dict = dict(zip(grp_names, matches_grps))

		if (attr_dict['model'] == 'EnsMean'):
			attr_dict['EnsType'] = f.split('/')[-3]
			attr_dict['model_type'] = 'EnsMean'
		else:
			attr_dict['model_type'] = 'Models'

		return attr_dict


	def retrieve(self, warn_if_not_exists=False, **kwargs):

		metric_name = self.__getattribute__(f'_{kwargs["metric"]}').metric

		if self.model == 'EnsMean':
			outdir = f'{self.outdir}/{self.model_type}/{self.EnsType}/{self.variable}/{metric_name}'
		else:
			outdir = f'{self.outdir}/{self.model_type}/{self.model}/{self.variable}/{metric_name}'

		f = f'{outdir}/{self.outname(**kwargs)}.nc'

		if not os.path.isfile(f) and warn_if_not_exists:
			warnings.warn('File Not Found!')

		return f

if __name__ == '__main__':

	f = get_model_year_combined_file('ACCESS1-0', 'pr', 'rcp45')
	m = NEXModel(f, outdir='/media/abhi/My_Passport/NEX-GDDP-NASA-PROCESSED')




	