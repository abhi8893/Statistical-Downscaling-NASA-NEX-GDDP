from metrics import Percentile, MeanMaxMin, ConsecDays, ThreshDays

class Metric():

    def __init__(self, **kwargs):
        self._percentile = Percentile(modelObj=self._modelObj)


        for method in ['tim', 'mon', 'year',
                       'yday', 'ymon', 'fld']:
            for stat in ['mean', 'max', 'min']:
                self.__dict__[f'_{method}{stat}'] = MeanMaxMin(stat=stat, method=method,
                                                         modelObj=self._modelObj)


        for index in ['cdd', 'cwd', 'chd', 'ccd']:
            self.__dict__[f'_{index}'] = ConsecDays(index=index, modelObj=self._modelObj)

        self._threshdays = ThreshDays(modelObj=self._modelObj)



    @property
    def _modelObj(self):
        return self


    def string(self, metric, **kwargs):
        return self.__getattribute__(f'_{metric}').string(**kwargs)


    def outname(self, metric, **kwargs):
        return self.__getattribute__(f'_{metric}').outname(obj=self, metric=metric, **kwargs)

    def cmd(self, metric, **kwargs):
        return self.__getattribute__(f'_{metric}').cmd(obj=self, **kwargs)

    def process(self, metric, **kwargs):
        return self.__getattribute__(f'_{metric}').process(metric=metric, **kwargs)
