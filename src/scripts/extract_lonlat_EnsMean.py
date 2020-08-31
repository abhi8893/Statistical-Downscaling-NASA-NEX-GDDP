from cdo import Cdo
import itertools
from helper_funcs import get_EnsMean_year_files
from multiprocessing import Pool
import os
from Model import *
cdo = Cdo()

OUTDIR = '/media/abhi/My_Passport/NEX-GDDP-NASA-OUTPUT/Amravati'
variables = ['pr', 'tasmax', 'tasmin']
scens = ['historical', 'rcp45', 'rcp85']


all_combs = list((list(tup) for tup in itertools.product(['EnsMean'], variables, scens, [[]])))

def extract_lonlat(f, outfile, lon=77.75, lat=20.93):
    ofile = cdo.remapnn(f'lon={lon}_lat={lat}',
                        input=f,
                        output=outfile,
                       options='--reduce_dim')
    
    return(ofile)


# pool = Pool()


for i, l in enumerate(all_combs[6:9]):
    args = l[0:4]
    files = get_EnsMean_year_files(*args[1:-1])
    all_combs[i][-1] = [None]*len(files)
    for j, f in enumerate(files):
        m = NEXModel(f)
        outdir = f'{OUTDIR}/{m.model}/{m.EnsType}/{m.variable}'
        os.system(f'mkdir -p {outdir}')
        outfile = f'{outdir}/{m.path.name}'
        all_combs[i][-1][j] = extract_lonlat(*[f, outfile])
    
# pool.close()
# pool.join()



