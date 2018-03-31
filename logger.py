""" Set and configure a local logger, called logger.
    Meant to be used through functions only...
"""

import logging

LEVEL = logging.DEBUG

# Initializing:
logger = logging.getLogger('this_logger')
logger.setLevel(LEVEL)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.info('Démarrage du logger')

# Logging functions
def logD(message):
    logger.debug(message)


def logI(message):
    logger.info(message)


def logW(message):
    logger.warning(message)


def logE(message):
    logger.error(message)


def logC(message):
    logger.critical(message)


if __name__ == '__main__':
    logD('Test de logger niveau DEBUG')
    logI('Test du logger niveau INFO')
    logW('Test du logger niveau WARNING')
    logE('Test du logger niveau ERROR')
    logC('Test du logger niveau CRITICAL')
