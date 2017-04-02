from ConfigParser import ConfigParser
import os

import appdirs

APP_NAME = "PresupuestoAbierto"
APP_AUTHOR = "PresupuestoAbierto"

def read_config(path):
    cp = ConfigParser()
    cp.read(path)

    # XXX TODO Validar config

    return {
        s: dict(cp.items(s)) for s in cp.sections()
    }

def appdir():
    """ Retorna el directorio donde deben estar los archivos de rafam_extract.
        Crea el directorio si no existe. """
    ad = appdirs.AppDirs(APP_NAME, APP_AUTHOR)
    config_dir = ad.user_config_dir

    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    return config_dir
