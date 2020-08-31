from analysis_help import get_kwargs, thresh_str, seas_str
from analysis_help import apply_kwargs, apply_op_chain
import re
import os
from cdo import Cdo
cdo = Cdo()


class Utility:

    keep_kwargs = ['variable', 'model', 'scen', 'year_str']

    def __init__(self, modelObj=None, **kwargs):
        for k in self.keep_kwargs:
            self.__dict__[k] = kwargs.get(k, None)

        self._modelObj = modelObj
        self._percentile = Percentile(modelObj=modelObj)

    def string(self, metric=None, **kwargs):
        return self.__getattribute__(f'_{metric}').string(**kwargs)

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
        outname_metric_str = self.string(**kwargs)
        outname_suffix = f"{arg_dict['model']}_{arg_dict['scen']}_{arg_dict['year_str']}"

        outname = '_'.join([outname_prefix, outname_metric_str, outname_suffix])

        return outname



    # metric independent
    def process(self, obj=None, cmd=None, output=None, metric=None, **kwargs):

        model_obj = self._modelObj \
                    if obj is None else obj


        cmd = self.cmd(metric=metric, **kwargs) if cmd is None else cmd
        
        # Refactor: This is too messy.
        p = re.compile(r'^[^\s]+')
        last_op_arg = p.findall(cmd)[0].split(',')
        op = last_op_arg[0]
        op = op[1:] if op.startswith('-') else op
        op = f'cdo.{op}'
        op = eval(op)

        try:
            arg = last_op_arg[1]
        except IndexError:
            arg = None

        if output == 'auto':
            outdir = f'{model_obj.outdir}/{model_obj.model}/{model_obj.variable}/{self.metric}'
            os.system(f'mkdir -p {outdir}')
            outname = kwargs['outname']
            output = f'{outdir}/{outname}.nc'


        if arg is not None:
            input_str = p.sub('', cmd, 1).strip()
            output = op(arg, input=input_str, output=output)


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




class Percentile(Utility):

    metric = 'percentile'


    def __init__(self, modelObj=None, **kwargs):
        super().__init__(**kwargs)
        self._modelObj = modelObj

    # metric dependent
    
    def string(self, pctl, method='tim', **kwargs):
        

        name = self.add_thresh_and_seas_string(f'{method}pctl{pctl}p',
                                          **kwargs) 
                        
        return name



    def _check_dependency(self, depends, file=None, obj=None):
        # TODO: check for self._percentile.depends

        model_obj = self._modelObj \
                    if obj is None else obj

        file = model_obj.file if file is None

        if depends is None:
            minfile, maxfile = file, file

        else:
            minfile, maxfile = depends['min'], depends['max']


        return minfile, maxfile

        

    def cmd(self, pctl,obj=None, method='tim',
            depends=None,
            op_chain=None, **kwargs):


        model_obj = self._modelObj \
                    if obj is None else obj

        file = apply_kwargs(model_obj.file, kwargs)
        file = apply_op_chain(file, op_chain)

        cmd = f'-{method}pctl,{pctl} {file} '

        minfile, maxfile = self._check_dependency(depends, file)


        cmd += f'-{method}min {minfile} '
        cmd += f'-{method}max {maxfile}'

        return cmd


class MeanMaxMin(Utility):

    metric = 'MeanMaxMin'

    # TODO: Add method arg in __init__
    def __init__(self, stat, modelObj=None, **kwargs):
        super().__init__(**kwargs)
        self.stat = stat
        self._modelObj = modelObj



    
    def string(self, method='tim', **kwargs):

        name = self.add_thresh_and_seas_string(f'{method}{self.stat}',
                                          **kwargs)

    def cmd(self, obj=None, method='tim',
            depends=None,
            op_chain=None, **kwargs):

        model_obj = self._modelObj \
                    if obj is None else obj


        file = apply_kwargs(model_obj.file, kwargs)
        file = apply_op_chain(file, op_chain)

        cmd = f'-{method}{self.stat} {file}'

        return cmd



class Metric():

    def __init__(self, **kwargs):
        self._percentile = Percentile(modelObj=self._modelObj)

        for metric in ['mean', 'max', 'min']:
            self.__dict__[f'_{metric}'] = MeanMaxMin(stat=metric, modelObj=self._modelObj)

    @property
    def _modelObj(self):
        return self


    def string(self, metric, **kwargs):
        return self.__getattribute__(f'_{metric}').string(**kwargs)


    def outname(self, metric, **kwargs):
        year_str = kwargs.get('year_str', self.year_str)
        return self.__getattribute__(f'_{metric}').outname(obj=self, metric=metric, **kwargs)

    def cmd(self, metric, **kwargs):
        return self.__getattribute__(f'_{metric}').cmd(obj=self, **kwargs)

    def process(self, metric, **kwargs):
        return self.__getattribute__(f'_{metric}').process(metric=metric, **kwargs)






    


