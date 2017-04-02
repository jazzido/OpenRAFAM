#!/usr/bin/env python
import os, platform, glob
from pip.req import parse_requirements
from rafam_extract import __version__
from setuptools import setup

if platform.system().startswith('Windows'):
    import py2exe

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'requirements.txt'),
                                  session=False)
# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

from distutils.core import setup

setup(name='rafam_extract',
      version=__version__,
      description='Copia datasets extraidos por Rafam_Db',
      author='Manuel Aristaran, Gaston Avila',
      author_email='jazzido@jazzido.com, avila.gas@gmail.com',
      url='https://github.com/jazzido/OpenRAFAM/',
      packages=['rafam_extract', ''],
      entry_points = {
        'console_scripts': ['rafam_extract=rafam_extract.command_line:main'],
      },
      options = {
        'py2exe': {
            'packages': ['rafam_db', 
                         'rafam_db.queries', 
                         'rafam_db.datasets', 
                         'rafam_db.dataset', 
                         'rafam_db.db',
                         'sqlalchemy.dialects'],
            'dll_excludes': ['oci.dll']
        }
      },
      data_files=[('.',  glob.glob(os.path.join(os.path.dirname(__file__),
                                   '../rafam_db/oracle_drivers/win32/*.dll')))],
      console=['rafam_extract/command_line.py'],
      install_requires=reqs)
