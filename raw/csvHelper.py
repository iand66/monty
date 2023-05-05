import csv, logging

def csvRead(filename:str, verbose:bool) -> list:
    '''
    Read CSV file
    :param filename - Fully qualified path to database name
    :param verbose - Enable verbose mode
    :return list or exception
    :example - csvRead('MyFileName.csv', True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    data = []
    try:
        with open(filename, encoding='utf8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(', '.join(row))
        if verbose:
            datlog.info(data)
        return data
    except Exception as e:
        applog.error(e)
        return e

def csvWrite(filename:str, data:list, verbose:bool) -> int:
    '''
    Write CSV file
    :param filename - Fully qualified path to OS directory
    :parma data - Data to write
    :param verbose - Enable verbose mode
    :return int - 1 Success or exception
    :example - csvWrite('MyFileName.csv', data, True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    try:
        with open(filename,'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            for i in range(len(data)):
                writer.writerow([data[i]])
        if verbose:
            datlog.info(data)
            #FIXME csvWrite Return boolean
        return 1
    except Exception as e:
        applog.error(e)
        return e

def csvDictReader(filename:str, verbose:bool) -> list:
    '''
    Read CSV file as dictionary
    :param filename - Fully qualified path to database name
    :param verbose - Enable verbose mode
    :return list or exception
    :example - csvDictReader('MyFileName.csv', True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    data = []
    try:
        with open(filename, encoding='utf8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        if verbose:
            datlog.info(data)
        return data
    except Exception as e:
        applog.error(e)
        return e

def csvDictWriter(filename:str, data:dict, verbose:bool) -> int:
    '''
    Write CSV file from dictionary
    :param filename - Fully qualified path to OS directory
    :parma data - Data to write
    :param verbose - Enable verbose mode
    :return int - 1 or exception
    :example - csvDictWriter('MyFileName.csv', data, True)
    '''
    applog = logging.getLogger('AppLog')
    datlog = logging.getLogger('DatLog')
    try:
        with open(filename, 'w', newline='', encoding='utf8') as f:
            fieldnames = data[0]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            if verbose:
                datlog.info(data)
                print(data)
        #FIXME csvDictWriter Return boolean
        return 1
    except Exception as e:
        applog.error(e)
        return e