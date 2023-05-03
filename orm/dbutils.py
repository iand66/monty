import logging
import os
import sqlalchemy

from raw.csvHelper import csvDictReader, csvRead
from sqlalchemy_utils import create_database, database_exists

from orm.dbfunctions import dbInsertAll
from orm.schema import *


def dbInit(engine:sqlalchemy.engine) -> int:
    '''
    Create database shell
    :param engine - SQLAlchemy engine instance
    :return int - 1 Success
    :example - dbInit(engine)
    '''
    applog = logging.getLogger('AppLog')
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
        applog.info(f'Database {engine.url} created at {datetime.today().strftime("%d-%m-%Y %H:%M")}')
        return 1
    else:
        for t in Base.metadata.sorted_tables:
            Base.metadata.create_all(engine, checkfirst=True)
        applog.info(f'Database {engine.url} updated at at {datetime.today().strftime("%d-%m-%Y %H:%M")}')
        return 1

def dbFill(engine:sqlalchemy.engine, seed:str, dbName:str, verbose:bool) -> int:
    '''
    Drop database & reload sample data from samples
    :param engine - SQLAlchemy engine instance
    :param seed - Fully qualified CSV file of files to import
    :param dbName - Database name
    :param verbose - Enable verbose mode
    :return int - 1 Success or 0 Failure
    :example - dbBuild(dbName, engine, False)
    '''
    applog = logging.getLogger('AppLog')
    #FIXME Try ... Except ... Logger?
    filesToImport = csvRead(seed, verbose)
    if filesToImport is not None:
        for f in enumerate(filesToImport):
            #FIXME Try ... Except ... Logger?
            dataToImport = csvDictReader(seed[0:seed.rfind('/')+1] + f[1], verbose)
            tblName = f[1][0:f[1].rfind('.')-1]
            dbInsertAll(engine, eval(tblName.title()), dataToImport, verbose)
        applog.info(f'{dbName} populated at {datetime.today().strftime("%d-%m-%Y %H:%M")}')
        return 1
    else:
        applog.error(f'Seed file of sample files could not be found')
        return 0

def dbKill(filename:str) -> int:
    '''
    Delete database
    :param filename - Fully qualified path to database name
    :return  - 1 Success 0 Failure
    :example - dbKill(dbName)
    '''
    applog = logging.getLogger('AppLog')
    if os.path.exists(filename):
       os.remove(filename)
       applog.info(f'File {filename} has been removed at {datetime.today().strftime("%d-%m-%Y %H:%M")}')
       if not os.path.exists(filename):
        return 1
    else:
       applog.warning(f'File {filename} could not be found')
       return 0