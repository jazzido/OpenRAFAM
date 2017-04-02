#!/usr/bin/env python
import os
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt'), session=False)

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

from setuptools import setup, find_packages
from rafam_db import __version__

setup(name='rafam_db',
      version=__version__,
      description='Extraer datos de una base de datos del sistema RAFAM',
      author='Manuel Aristaran, Gaston Avila',
      author_email='jazzido@jazzido.com, avila.gas@gmail.com',
      url='https://github.com/jazzido/OpenRAFAM/',
      packages=['rafam_db'],
      zip_safe=False,
      install_requires=reqs)
