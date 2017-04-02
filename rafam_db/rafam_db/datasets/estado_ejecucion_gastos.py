# coding: utf-8
import re

from rafam_db.dataset import DataSet

class EstadoEjecucionGastos(DataSet):
    """
    Dataset de estado de ejecucion del presupuesto de gastos
    """

    def parse_parameters(self, **kwargs):
        super(EstadoEjecucionGastos, self).parse_parameters(**kwargs)
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
            elif k == 'confirmado':
                if v.upper() not in ('S', 'N'):
                    raise ParameterException, "confirmado debe ser S o N"
                else:
                    parsed_parameters[k] = v.upper()
            else:
                # el resto (si hubiera) pasan como vienen
                parsed_parameters[k] = v

        # chequear que date_from y date_to sean del año 'year'
        if int(parsed_parameters['date_from'][:4]) !=  parsed_parameters['year'] \
           or int(parsed_parameters['date_to'][:4]) !=  parsed_parameters['year']:
            raise ParameterException, "el año de `date_from` y `date_to` tiene que ser igual al parametro `year`"

        return parsed_parameters
