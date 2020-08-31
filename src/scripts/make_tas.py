from helper_funcs import get_template_file
from cdo import Cdo
cdo = Cdo()

scen = ['historical', 'rcp45', 'rcp85']
model = 'EnsMean_ALL21'

for scen_name in scen:
    f = {}
    for var_name in ['tasmax', 'tasmin', 'tas']:
        f[var_name] = get_template_file(model, var_name, scen_name)

    cdo.mulc('2', input=f"-add {f['tasmax']} {f['tasmin']}", output=f['tas'])