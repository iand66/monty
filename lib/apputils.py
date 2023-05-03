import configparser
import logging, sys, os
import datetime as dt
from logging.config import fileConfig

def config(filename:str) -> configparser:
    '''
    Read configurable parameters from INI file
    :param filename - Fully qualifed path to INI file
    :return config - ConfigParser object
    :example - c = config('MyConfigFilePath.ini')
    '''
    config = configparser.ConfigParser()

    try:
        config.read_file(open(filename,'r'))
    except Exception as e:
        print(f'Could not find {filename} file')
        sys.exit()
    return config

def logSetup(logcfg:str, logloc:str, echo:bool) -> logging.Logger:
    '''
    Setup application & database level logging
    :param logcfg - Fully qualified location of logging config file
    :param logloc - Directory to store application log files
    :param echo - Propagate application logs to console
    :return logger - Updated logger object
    :example - logger = logSetup('./ini/logger.ini', './logs/', False)
    '''
    today = dt.datetime.today()
    logfile = logloc + f'{today.year}-{today.month:02d}-{today.day:02d}.log'
    datfile = logloc + f'{today.year}-{today.month:02d}-{today.day:02d}.trc'

    try:
        os.path.exists(logcfg)
    except Exception as e:
        print(f'Could not find {logcfg} file')
        sys.exit()

    try:
        fileConfig(logcfg, defaults={'logfilename':logfile,'datfilename':datfile})
        logger = logging.getLogger('AppLog')
        logger.propagate=echo
        logger = logging.getLogger('DatLog')
        logger.propagate=echo
    except Exception as e:
        print(f'Could not parse {logcfg} file')
        sys.exit()
    return logger

