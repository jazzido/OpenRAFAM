# coding: utf-8

from abc import ABCMeta
import os
import sys
import importlib
from datetime import date, datetime
import re
import json
import decimal

import sqlparse
import unicodecsv

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError

class ParameterException(Exception):
    pass

class DataSet(object):
    """
    Abstract base class for DataSet
    """

    __metaclass__ = ABCMeta

    def __init__(self, engine):
        self.name = None
        self.rows = None
        self.query = self.__class__.get_query()
        self.rafam_version = None
        self.engine = engine

    def scrape(self, **kwargs):
        if self.query is None:
            raise NotImplementedError('')

        parsed_parameters = self.parse_parameters(**kwargs)

        self.date = date.today().strftime('%Y-%m-%d')
        self.rows = self.engine.execute(self.query, **parsed_parameters) #.fetchall()
        return self.rows

    def parse_parameters(self, **kwargs):
        """
        el comportamiento por default de parse_parameters
        es chequear la presencia de los parametros requeridos
        Si un DataSet tiene que transformar los parametros que recibe,
        redefinir este metodo en la subclase.
        Ver EstadoEjecucion como ejemplo.
        """
        required_params = self.__class__.get_parameters()
        if set(kwargs.keys()) != required_params:
            raise ParameterException, "Parametros requeridos: %s" % (', '.join(list(required_params)))

        return kwargs

    @classmethod
    def all_datasets(cls):
        return [(c, c.__doc__) for c in cls.__subclasses__()]

    @classmethod
    def get_query(cls):
        """ obtiene el query para este :class:DataSet """
        mod = importlib.import_module('.%s' % cls.__name__,
                                      'rafam_db.queries')
        return mod.QUERY

    @classmethod
    def get_parameters(cls):
        """ obtiene los parametros de self.query """
        placeholders = set([p.value[1:] # sacar el ':' inicial
                           for p in filter(lambda t: t.ttype == sqlparse.tokens.Token.Name.Placeholder,
                                           sqlparse.parse(cls.get_query())[0].flatten())])
        return placeholders

    def toCSV(self, out=sys.stdout):
        "Saves dataset rows to a CSV file"
        fieldnames = self.rows.keys()

        writer = unicodecsv.DictWriter(out, fieldnames)
        writer.writeheader()
        for r in self.rows:
            writer.writerow(dict(r))

    def toJSONLINES(self, out=sys.stdout):
        for r in self.rows:
            print >>out, json.dumps(dict(r), default=decimal_default)

from . datasets import *
