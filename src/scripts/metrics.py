from Utility import Utility
from analysis_help import get_kwargs, apply_kwargs
from analysis_help import apply_op_chain
from cdo import Cdo
import re
cdo = Cdo()

default = {}

default['units'] = {'pr': 'mm',
                    'tas': 'C',
                    'tasmax': 'C',
                    'tasmin': 'C'}

class Percentile(Utility):

    metric = 'percentile'


    def __init__(self, modelObj=None, **kwargs):
        super().__init__(**kwargs)
        self._modelObj = modelObj

    
    def string(self, pctl, method='tim', **kwargs):
        

        name = self.add_thresh_and_seas_string(f'{method}pctl{pctl}p',
                                          **kwargs) 
                        
        return name



    def _check_dependency(self, depends, file=None, obj=None):
        # TODO: check for self._percentile.depends

        model_obj = self._modelObj \
                    if obj is None else obj

        file = model_obj.file if file is None else file

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

        func_kwargs = {'thresh': dict(set_miss_range_to='missval')}

        file = apply_kwargs(model_obj.file, kwargs, **func_kwargs)
        file = apply_op_chain(file, op_chain)

        cmd = f'-{method}pctl,{pctl} {file} '

        if depends is None:
            cmd += f'-{method}min {file} '
            cmd += f'-{method}max {file}'

        else:

            minfile, maxfile = self._check_dependency(depends, file)

            cmd += f'{minfile} {maxfile}'

        return cmd


class MeanMaxMin(Utility):


    # TODO: Add method arg in __init__
    def __init__(self, stat, method, modelObj=None, **kwargs):
        super().__init__(**kwargs)
        self.stat = stat
        self._modelObj = modelObj
        self.method = method
        self.metric = f'{self.__class__.__name__}_{method}'



    
    def string(self, **kwargs):

        name = self.add_thresh_and_seas_string(f'{self.method}{self.stat}',
                                          **kwargs)

        return name

    def cmd(self, obj=None,
            depends=None,
            op_chain=None, **kwargs):

        model_obj = self._modelObj \
                    if obj is None else obj

        func_kwargs = {'thresh': dict(set_miss_range_to=0)}
        file = apply_kwargs(model_obj.file, kwargs, **func_kwargs)
        file = apply_op_chain(file, op_chain)

        cmd = f'-{self.method}{self.stat} {file}'

        return cmd


class ConsecDays(Utility):


    def __init__(self, index, modelObj=None, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self._modelObj = modelObj
        self.metric = self.__class__.__name__


    def string(self, index_kwargs, **kwargs):
        thresh, ndays = index_kwargs['thresh'], index_kwargs['ndays']
        units = default['units'][self._modelObj.variable]

        name = self.add_thresh_and_seas_string(f'{self.index}{thresh}{units}{ndays}D',
                                          **kwargs)

        return name

    def cmd(self, index_kwargs, 
            obj=None, op_chain=None, **kwargs):

        model_obj = self._modelObj \
                    if obj is None else obj

        file = apply_kwargs(model_obj.file, kwargs)
        file = apply_op_chain(file, op_chain)

        if self.index == 'chd':
            metric_op = 'cwd'
        elif self.index == 'ccd':
            metric_op = 'cdd'
        elif self.index in ['cwd', 'cdd']:
            metric_op = self.index

        thresh, ndays = index_kwargs['thresh'], index_kwargs['ndays']
        cmd = f'-eca_{metric_op},{thresh},{ndays} {file}'


        return(cmd)


class ThreshDays(Utility):

    def __init__(self, modelObj=None, **kwargs):
        super().__init__(**kwargs)
        self._modelObj = modelObj
        self.index = 'threshdays'
        self.metric = self.__class__.__name__


    def string(self, index_kwargs, **kwargs):
        thresh = index_kwargs['thresh']
        units = default['units'][self._modelObj.variable]

        name = self.add_thresh_and_seas_string(f'{self.index}{thresh}{units}',
                                          **kwargs)

        return name


    def cmd(self, index_kwargs,
            obj=None, op_chain=None, **kwargs):

        model_obj = self._modelObj \
                    if obj is None else obj


        file = apply_kwargs(model_obj.file, kwargs)
        file = apply_op_chain(file, op_chain)

        thresh = index_kwargs['thresh']
        cmd = f'-mulc,100 -timmean -gtc,{thresh} {file}'

        return(cmd)







