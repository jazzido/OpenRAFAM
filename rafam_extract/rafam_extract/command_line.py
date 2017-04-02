# coding: utf-8

# No cambies este docstring si no sabés lo que estás haciendo.
# El docstring es la definición de la sintaxis de los argumentos
# del ejecutable
# https://github.com/docopt/docopt
"""Rafam_Extract.

Usage:
  rafam_extract test_rafam [-c INI_FILE]
  rafam_extract datasets
  rafam_extract extract <dataset> [-p param...] [-c INI_FILE] [-o FILE] [-f FORMAT]
  rafam_extract --version

Options:
  -h --help                       Show this screen.
  --version                       Show version.
  -o FILE --output FILE           Output file. Default is STDOUT
  -p PARAM --param PARAM          Parameter name and value. Eg: date=2015-07-09
  -f FORMAT --format FORMAT       Output format (JSONLINES, CSV. Default is CSV)
  -c INI_FILE --config INI_FILE   Path to INI file (optional)
"""
import os, sys, re, traceback, contextlib

from docopt import docopt

from rafam_extract import config, __version__
from rafam_db import dataset, db

PARAM_RE = re.compile(r'^(?P<param>[A-Za-z_]+)=(?P<value>[\S]+)$')
FORMATTERS = {
    'JSONLINES': 'toJSONLINES',
    'CSV': 'toCSV'
}

def read_ini(ini_path=None):
    if ini_path is None:
        ini_path = os.path.join(config.appdir(), '%s.ini' % config.APP_NAME)

    if not os.path.isfile(ini_path):
        raise IOError, "%s does not exist" % ini_path

    c = config.read_config(ini_path)

    return c

def create_engine(ini_path):
    conf = read_ini(ini_path)
    db_conf = conf['Database']
    engine = db.init_engine(db_conf['username'],
                            db_conf['password'],
                            db_conf['host'],
                            db_conf['sid'])
    return engine

def perror(err):
    print >>sys.stderr, "ERROR: %s" % err


def main():
    arguments = docopt(__doc__, version="Rafam_Extract %s" % __version__)

    try:
        if arguments.get('test_rafam'):
            try:
                engine = create_engine(arguments.get('--config'))
            except IOError as e:
                print >>sys.stderr, e
                return 1
            test_rafam(engine)
        elif arguments.get('datasets'):
            datasets()
        elif arguments.get('extract'):
            # check that INI exists and create engine
            try:
                engine = create_engine(arguments.get('--config'))
            except IOError as e:
                print >>sys.stderr, e
                return 1

            # check that dataset exists
            ds = [d for d, _ in dataset.DataSet.all_datasets()
                  if d.__name__ == arguments.get('<dataset>')]
            if len(ds) == 0:
                perror("El Dataset `%s` no existe" % arguments.get('<dataset>'))
                return 1

            # check that format is valid
            format_ = arguments.get('--format')
            format_ = format_ if format_ is not None else 'CSV'
            if format_ not in FORMATTERS.keys():
                perror("`%s` no es un formato válido" % format_)
                return 1

            out = arguments.get('--output')
            if out is None:
                out = sys.stdout
            else:
                out = open(out, 'wb')

            ds = ds[0]
            ds_params = ds.get_parameters()
            # parse parameters
            params = {}
            for pstring in arguments.get('--param'):
                 m = PARAM_RE.match(pstring.strip())
                 if m is None:
                     perror("Error en formato de parámetro. Usar param_name=value")
                     return 1
                 mg = m.groupdict()

                 if mg['param'] not in ds_params:
                     perror("Parámetro desconocido `%s` para el dataset `%s`" % (mg['param'], ds.__name__))
                     return 1

                 params[mg['param']] = mg['value']
            try:
                extract(engine, ds, format_, out, **params)
            except dataset.ParameterException as e:
                perror(e)
                return 1
            finally:
                if out is not sys.stdout:
                    out.close()
        return 0
    except Exception as e:
        print >>sys.stderr, e
        traceback.print_exc(file=sys.stdout)
        return 1

def extract(engine, dataset, format_, out, **params):
    ds = dataset(engine)
    ds.scrape(**params)
    formatter_method = FORMATTERS[format_]
    getattr(ds, formatter_method)(out)

def test_rafam(engine):
    """ Verifica la conexión a la base de datos RAFAM """
    vr = dataset.VersionesRafam(engine)
    print "Subsistemas RAFAM:"
    for row in vr.scrape():
        print "  - %s %s - v%s (%s)" % (row[0], row[1], row[2], row[3].strftime('%Y-%m-%d'))
    print

def datasets():
    print "Datasets disponibles:"
    for ds, doc in dataset.DataSet.all_datasets():
        print "  - %s\n    %s" % (ds.__name__, doc.strip())
        print "    Parametros: %s" % (', '.join(ds.get_parameters()))
        print
    print

if __name__ == '__main__':
    sys.exit(main())
