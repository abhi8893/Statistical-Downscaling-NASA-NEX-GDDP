from helper_funcs_download import download_file, get_url
import pandas as pd
import os
from tqdm import tqdm

files_status = pd.read_csv('pickles/check-model-files/files_status.csv')
to_download = files_status.loc[files_status.status != "OK"]
num_files = to_download.shape[0]

def get_outdir(model, variable, prefix='.', makedir=False):
    outdir = f'{prefix}/{model}/{variable}'
    if makedir:
        os.system(f'mkdir -p {outdir}')

    return outdir

files_status = [None]*num_files
i=0
for index, row in tqdm(to_download.iterrows()):
    fields = ['year', 'model', 'variable', 'scen']
	
    year, model, variable, scen = [row[field] for field in fields]
    outdir = get_outdir(model, variable, prefix='output/missing_NEX-GDDP_files', makedir=True)
    status = download_file(year, model, variable, scen, outdir=outdir)
    files_status[i] = status
    i += 1
    
files_status = list(filter(None, files_status))
to_download.loc[:, 'status'] = files_status

outdir = 'pickles/download_missing'
os.system(f'mkdir -p {outdir}')
to_download.to_csv(f'{outdir}/last_down_status.csv', index=False)

