from helper_funcs import *	
from multiprocessing import Pool, cpu_count
import pandas as pd



def expected_num_files(m, v, scen):
    if scen == "historical":
        n_h = 1
        n_f = 0
    elif scen == "future":
        n_h = 0
        n_f = 1
    elif scen == "both":
        n_h = 1
        n_f = 1
    elif scen == "all":
        n_h = 1
        n_f = 2
        
    exp_val = m*v*n_h*(2005-1950 +1) + m*v*n_f*(2099-2006 +1)
    
    return(exp_val)

class DummyFile:
    def __init__(self, status):
        self.status = status
    
    def get(self):
        return self.status


files_status = [None]*expected_num_files(21, 3, "all")

counter=0
for model in possibilities['model']:
    for variable in possibilities['variable']:
        for scen in possibilities['scen']:
            if scen == "historical":
                years = range(1950, 2005 + 1)
            else:
                years = range(2006, 2099 + 1)

            for year in years:
                args = [year, model, variable, scen]
                try:
                    f = get_model_year_file(*args)[0]
                    status = check_file(f)
                except IndexError:
                    status = 'missing'
                    
                files_status[counter] = (args + [status])
                
                counter += 1



files_status = list(filter(None, files_status))
df = pd.DataFrame(files_status, columns=['year', 'model', 'variable', 'scen', 'status'])
# df.status = df.status.apply(lambda x: x.get())

outdir = "pickles/check-model-files"
os.system(f'mkdir -p {outdir}')
df.to_csv(f'{outdir}/files_status.csv', index=False)

