# coding: utf-8
import re

from rafam_db.dataset import DataSet

class EstadoEjecucionRecursos(DataSet):
    """
    Dataset del estado de ejecucion de los recursos
    """
    def parse_parameters(self, **kwargs):
        super(EstadoEjecucionRecursos, self).parse_parameters(**kwargs)
        parsed_parameters = {}

        for k, v in kwargs.iteritems():
            if k in ('date_from', 'date_to'):
                if re.match('^\d\d\d\d-\d\d-\d\d$', v):
                    parsed_parameters[k] = v
                else:
                    raise ParameterException, "%s debe tener formato YYYY-MM-DD" % k
            elif k == 'year':
                if re.match('^\d\d\d\d$', v):
                    parsed_parameters[k] = int(v)
                else:
                    raise ParameterException, "year debe tener formato YYYY"
            else:
                # el resto (si hubiera) pasan como vienen
                parsed_parameters[k] = v

        return parsed_parameters
