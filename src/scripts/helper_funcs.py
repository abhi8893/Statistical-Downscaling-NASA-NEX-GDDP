from cdo import Cdo
import xarray as xr
import os
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull
import sys
from pathlib import Path
import glob
import difflib
from collections import OrderedDict
import re
import glob

cdo = Cdo()

DATA_DIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA')
DATA_DIR_COMBINED = Path('/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/model_year_combined')
OUT_DIR = Path('/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT')
os.system(f'mkdir -p "{OUT_DIR}"')

models =   [dI for dI in os.listdir(DATA_DIR) 
           if os.path.isdir(os.path.join(DATA_DIR,dI))]

variables = ['pr', 'tasmax', 'tasmin']
scen = ['historical', 'rcp45', 'rcp85']
scen_year_str = dict(zip(scen, ['1950-2005', '2006-2099', '2006-2099']))

possibilities = OrderedDict({'model': models,
                             'variable': variables,
                             'scen': scen})

def get_apt_names(model, variable, scen):
    model, variable, scen = [difflib.get_close_matches(word, possible, n=1, cutoff=0)[0]
                             for word, possible in zip([model, variable, scen], 
                                                       possibilities.values())]
    
    return [model, variable, scen]

def get_model_files(model, variable, scen, model_data_dir=DATA_DIR):
    model, variable, scen = get_apt_names(model, variable, scen)
    files = glob.glob(f'{model_data_dir}/{model}/{variable}/*{scen}*.nc')
    files_year = list(map(lambda x: x.split('_')[-1], files))
    sorted_files = [f for _, f in sorted(zip(files_year, files))]
    
    return sorted_files

def get_model_year_file(year, model, variable, scen, model_data_dir=DATA_DIR):
    model, variable, scen = get_apt_names(model, variable, scen)
    files = glob.glob(f'{model_data_dir}/{model}/{variable}/{variable}_day_{model}_{scen}_r1i1p1_{year}.nc')
    if len(files) == 0:
        files = glob.glob(f'{model_data_dir}/{model}/{variable}/{variable}_day_{model.lower()}_{scen}_r1i1p1_{year}.nc')
        if len(files) == 0:
            files = ['']

    return files

def get_EnsMean_year_files(variable, scen, Ens_type='ALL21'):
    dir_1 = 'EnsMean_yearwise'
    dir_2 = Ens_type
    data_dir = f'{OUT_DIR}/{dir_1}/{dir_2}/{variable}'

    files = glob.glob(f'{data_dir}/{variable}*{scen}*')
    files_year = list(map(lambda x: x.split('_')[-1], files))
    sorted_files = [f for _, f in sorted(zip(files_year, files))]

    return sorted_files






def make_year_combined_file(model, variable, scen, outdir=None):
    
    model, variable, scen = get_apt_names(model, variable, scen)

    model_files = get_model_files(model, variable, scen)
    
    # Make outdir
    if (outdir is None):
        outdir = f'{OUT_DIR}/model_year_combined/{model}/{variable}'

    os.system(f'mkdir -p {outdir}')
    any_file = model_files[0]
    ens_id =  Path(any_file).name.split('_')[-2]

    
    cmd = ' '.join(model_files)
    
    outname = '_'.join([variable, 'day', model, scen, '1950-2005.nc'])
    outfile = f"{outdir}/{outname}"

    cdo.mergetime(input=cmd,
                  output=f"{outdir}/tmp.nc",
                 env={"SKIP_SAME_TIME": "1"})
    
    if variable == "pr":
        cdo.mulc('86400', input=f"{outdir}/tmp.nc",
                output=outfile)
        
    elif variable in ['tasmax', 'tasmin']:
        cdo.addc('-273.15', input=f"{outdir}/tmp.nc",
                output=outfile)        
    
    os.system(f'rm {outdir}/tmp.nc')
    
    return(outfile)


def get_model_year_combined_file(model, variable, scen):

    data_dir = get_data_dir(model)
    return glob.glob(f'{data_dir}/{variable}/*{scen}*')[0]


def get_template_file(model, variable, scen):
    year_str = scen_year_str[scen]
    dir_1, dir_2 = get_dirs(model)

    data_dir = get_data_dir(model)
    fname = f'{variable}_day_{dir_1}_{scen}_{year_str}'

    f = f'{data_dir}/{variable}/{fname}.nc'

    return f






@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


def check_file(f):
    exists = os.path.isfile(f)
    if not exists:
        msg = 'missing'
    else:
        with suppress_stdout_stderr():
            try:
                res = cdo.sinfov(input=f)
                msg = "OK"
            except Exception:
                msg = "corrupted"
    
    return msg

def get_dirs(model):
    if re.match(re.compile('EnsMean_.*'), model):                          
        dir_1, dir_2 = model.split('_')
    else:
        dir_1, dir_2 = ['Models', model]

    return [dir_1, dir_2]



def get_data_dir(model):
    dir_1, dir_2 = get_dirs(model)
        
    data_dir = f'{OUT_DIR}/{dir_1}/{dir_2}'
        
    return data_dir


