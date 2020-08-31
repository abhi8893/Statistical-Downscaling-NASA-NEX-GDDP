import os
from helper_funcs import suppress_stdout_stderr, check_file
import subprocess


def get_url(year, model, variable, scen):
	url = f'ftp://cccr.tropmet.res.in/iRODS_DATA/INDO-US2017/NEX-GDDP-INDIA/{model}/{variable}/{variable}_day_{model}_{scen}_r1i1p1_{year}.nc'
	return url
	
	
def download_file(year, model, variable, scen, outdir='.', print_msg=True, user='cordexsa', pswd='CORDEXCCCR17'):
	url = get_url(year, model, variable, scen)
	wget_cmd = f'wget --user {user} --password {pswd} '
	wget_cmd += url
	wget_cmd += f' -P {outdir}'
	
	if print_msg:
		os.system(wget_cmd)
	else:
		subprocess.check_output(wget_cmd)
			
	outname = url.split('/')[-1]
	outfile = f"{outdir}/{outname}"
	
	return check_file(outfile)
    







