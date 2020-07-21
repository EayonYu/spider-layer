name = 'spider'


import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from easylog import get_logger


logger = get_logger()
logger.info().msg("websocket layer")
