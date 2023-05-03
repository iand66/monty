from sqlalchemy import create_engine
from lib.apputils import config, logSetup

if __name__ == '__main__':
    appcfg = config('./ini/globals.ini')
    logger = logSetup(appcfg['LOGCFG']['logcfg'], appcfg['LOGCFG']['logloc'], eval(appcfg['LOGCFG']['logecho']))
    engine = create_engine(appcfg['DBCFG']['dbType'] + appcfg['DBCFG']['dbName'])
