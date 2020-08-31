from analysis_help import get_kwargs, apply_kwargs
from analysis_help import apply_op_chain
from analysis_help import thresh_str, seas_str
import re
import os
import uuid
from cdo import Cdo
cdo = Cdo()


class Utility:

    keep_kwargs = ['variable', 'model', 'scen', 'year_str']

    def __init__(self, modelObj=None, **kwargs):
        for k in self.keep_kwargs:
            self.__dict__[k] = kwargs.get(k, None)

        self._modelObj = modelObj

    def string(self, metric=None, **kwargs):
        return ''

    # metric independent
    def outname(self,
                obj=None, 
                variable=None, 
                model=None, scen=None, year_str=None, metric=None, **kwargs):


        model_obj = self._modelObj \
                    if obj is None else obj

        arg_dict = dict(zip(['variable', 'model', 'scen', 'year_str'],
                            [variable, model, scen, year_str]))

        # Refactor: Better name?
        arg_dict = {k: model_obj.__dict__[k] if v is None else v
                    for k, v in arg_dict.items()}

        outname_prefix = f"{arg_dict['variable']}"
        outname_metric_str = model_obj.string(metric, **kwargs)
        outname_suffix = f"{arg_dict['model']}_{arg_dict['scen']}_{arg_dict['year_str']}"

        outname = '_'.join([outname_prefix, outname_metric_str, outname_suffix])

        return outname



    # metric independent
    def process(self, obj=None, cmd=None, outdir=None, 
                metric=None, outname=None, **kwargs):

        model_obj = self._modelObj \
                    if obj is None else obj


        cmd = model_obj.cmd(metric=metric, **kwargs) if cmd is None else cmd
        
        # Refactor: This is too messy.
        p = re.compile(r'^[^\s]+')
        last_op_arg = p.findall(cmd)[0].split(',')
        op = last_op_arg[0]
        op = op[1:] if op.startswith('-') else op
        op = f'cdo.{op}'
        op = eval(op)

        try:
            arg = ','.join(last_op_arg[1:])
        except IndexError:
            arg = None


        if outdir is None and outname is None:
            output = None

        else: 
            if outdir is not None:
                if outdir == 'auto':
                    if model_obj.model == 'EnsMean':
                        outdir = f'{model_obj.outdir}/{model_obj.model_type}/{model_obj.EnsType}/{model_obj.variable}/{self.metric}'
                    else:
                        outdir = f'{model_obj.outdir}/{model_obj.model_type}/{model_obj.model}/{model_obj.variable}/{self.metric}'

                os.system(f'mkdir -p {outdir}')
            else:
                outdir = '/tmp'


            

            if outname is not None:
                if outname == 'auto':
                    outname = model_obj.outname(metric=metric, **kwargs)
            else:
                # TODO: 1. Metric name
                #       2. Shorter random name
                outname = f'{self.metric}_{uuid.uuid4().hex}'


            output = f'{outdir}/{outname}.nc'




        input_str = p.sub('', cmd, 1).strip()

        if arg is not None:
            output = op(arg, input=input_str, output=output)
        else:
            output = op(input=input_str, output=output)


        return output

    @staticmethod
    def add_thresh_and_seas_string(name, **kwargs):
        seas, thresh, thresh_type = get_kwargs(kwargs, 
                                               ['seas', 'thresh', 'thresh_type'])


        # Note: name is a string hence immutable
        # i.e. won't affect the name passed
        name += f'-{thresh_str(thresh, thresh_type)}'\
                if thresh is not None else ''
        name += f'-{seas_str(seas)}'

        return name     
