__version__ = '0.0.1'

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s -- %(message)s',
                    handlers=[logging.StreamHandler()])
