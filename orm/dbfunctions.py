import logging
import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from orm.schema import *

# Table level functions
def dbInsertAll(engine:sqlalchemy.engine, tblName:str, data:Base, verbose:bool) -> int:
    '''
    Insert multiple records into database table
    :param engine - SQLAlchemy engine instance
    :param tblName - Database tablename 
    :param data - SQLALchemy data objects
    :parma verbose - Enable verbose mode
    :return int - Number of records inserted or exception
    :example - dbInsertAll(engine, eval(tblName.title()), dataToImport, verbose)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    with Session(engine) as session:
        if engine.name == 'sqlite':
            session.execute('pragma foreign_keys=on')
        try:
            session.bulk_insert_mappings(tblName, data)
            session.commit()
            if verbose:
                datlog.info(data)
            return len(data)
        except Exception as e:
            session.rollback()
            applog.error(e)
            return e

def dbSelectAll(engine:Session, tblName:Base, verbose:bool) -> list:
    '''
    Select all records from a database table
    :param engine - SQLAlchemy engine instance
    :param tblName - Database tablename 
    :param verbose - Enable verbose mode
    :return data - Query results as list
    :example - x = dbSelectAll(engine, Genre, True)
    '''
    #FIXME DBAPI Events
    datlog = logging.getLogger('DatLog')
    with Session(engine) as session:
        data = []
        results = session.query(tblName).all()
        for row in results:
            rowdict = {col: str(getattr(row,col)) for col in row.__table__.c.keys()}
            if verbose:
                datlog.info(f'Selected ... {rowdict}')
            data.append(rowdict)
        return data

def dbUpdateAll(engine:Session, tblName:Base, updAttr:str, updVal:str, verbose:bool) -> int:
    '''
    Update unfiltered records in a database table
    :param engine - SQLAlchemy engine instance
    :param tblName - Database tablename 
    :param updAttr - Table column to update
    :param updVal - New value for table column
    :param verbose - Enable verbose mode
    :return results - Integer of update results processed
    :example - x = dbUpdateAll(engine, Customer, 'City', 'My Town', True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    with Session(engine) as session:
        try:
            results = session.query(tblName).update({updAttr:updVal})
            session.commit()
            if verbose:
                datlog.info(f'Updated {tblName.__tablename__} table, {updAttr} column contents, to "{updVal}" {results} times')
            return results
        except Exception as e:
            session.rollback()
            applog.error(e)
            return(e)

def dbDeleteAll(engine:Session, tblName:Base, verbose:bool) -> int:
    '''
    Delete all records from table
    :param engine - SQLAlchemy engine instance
    :param tblName - Database tablename 
    :param filters - Dictionary ColumnName Criteria
    :param verbose - Enable verbose mode
    :return int - Number of records deleted
    :example - dbDeleteAll(engine, Customer, True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog') 
    with Session(engine) as session:
        if engine.name == 'sqlite':
            session.execute('pragma foreign_keys=on')
        try:
            results = session.query(tblName).delete()
            session.commit()
            if verbose:
                datlog.info(f'Deleted {tblName.__tablename__} contents ... {results} entries')
            return results
        except Exception as e:
            session.rollback()
            applog.error(e)
            return(e)

# Record level functions
def dbInsert(engine:Session, data:Base, verbose:bool) -> int:
    '''
    Insert record into database table
    :param engine - SQLAlchemy engine instance
    :param data - SQLALchemy data object 
    :param verbose - Enable verbose mode
    :return int - RowId of inserted record
    :example - dbInsert(engine,Genre(GenreName='Screaming'),True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    with Session(engine) as session:
        if engine.name == 'sqlite':
            session.execute('pragma foreign_keys=on')
        try:
            session.add(data)
            session.commit()
            session.refresh(data)
            if verbose:
                datlog.info(f'Added record number {data.Id} to {data.__tablename__}')
            return data.Id
        except Exception as e:
            session.rollback()
            applog.error(e)

def dbSelect(engine:Session, tblName:Base, filters:dict, verbose:bool) -> list:
    '''
    Select records from a database table
    :param engine - SQLAlchemy engine instance
    :param tblName - Database tablename 
    :param filters - Dictionary {'ColumnName':'Criteria'}
    :param verbose - Enable verbose mode
    :return data - Query results as list
    :example - x = dbSelect(engine, Customer, {'Country':'Brazil' [,...]}, True)
    '''
    #FIXME Rethink
    datlog = logging.getLogger('DatLog')
    with Session(engine) as session:
        data = []
        results = session.query(tblName).filter_by(**filters).all()
        if len(results) > 0:
            for row in results:
                rowdict = {col: str(getattr(row,col)) for col in row.__table__.c.keys()}
                data.append(rowdict)
                if verbose:
                    datlog.info(f'Selected ... {rowdict}')
            return data
        else:
            datlog.info(f'Missing ... {filters}')

def dbUpdate(engine:Session, tblName:Base, filters:dict, updAttr:str, updVal:str, verbose:bool) -> int:
    '''
    Update filtered records in a database table
    :param engine - SQLAlchemy engine instance
    :param tblName - Database tablename 
    :param filters - Dictionary {'ColumnName':'Criteria' [,...]}
    :param updAttr - Table column to update
    :param updVal - New value for table column
    :param verbose - Enable verbose mode
    :return results - Integer of update results processed
    :example - x = dbUpdate(engine, Customer, {'Country':'Brazil'}, 'City', 'My Town', True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    with Session(engine) as session:
        try:
            results = session.query(tblName).filter_by(**filters).update({updAttr:updVal})
            session.commit()
            if verbose:
                datlog.info(f'Updated {tblName.__tablename__} table, {updAttr} column contents, to "{updVal}" {results} times')
            return results
        except Exception as e:
            session.rollback()
            applog.error(e)
            return e

def dbDelete(engine:Session, tblName:Base, filters:dict, verbose:bool) -> int:
    '''
    Delete records from a database table
    :param engine - SQLAlchemy engine instance
    :param tblName - Database tablename 
    :param filters - Dictionary ColumnName Criteria
    :param verbose - Enable verbose mode
    :return int - Number of records deleted
    :example - dbDelete(engine, Customer, {'Country':'Brazil'}, True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    with Session(engine) as session:
        if engine.name == 'sqlite':
            session.execute('pragma foreign_keys=on')
        try:
            results = session.query(tblName).filter_by(**filters).delete()
            session.commit()
            if verbose:
                datlog.info(f'Deleted {list(filters.keys())[0]} = {list(filters.values())[0]} from {tblName.__tablename__} table {results} times')
            return results
        except Exception as e:
            applog.error(e)
            return e
            