import mysql.connector

cnx = ''

def ParseTableNames(database):
    tablenames = []
    parse_execute = "Select `COLUMN_NAME` from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='" + database + "';"
    cursor = cnx.cursor()
    cursor.execute(parse_execute)
    for db in cursor.fetchall():
        for d in db:
            tablenames.append(d)
    print(tablenames)
    return tablenames

def ParseTables(database, YMD, table):
    parse_execute = 'SELECT * FROM ' + database + '.`' + table + '` WHERE `Дата создания` BETWEEN "' + YMD + ' 00:00:00" AND "' + YMD + ' 23:59:59";'
    strings = []
    cursor = cnx.cursor()
    cursor.execute(parse_execute)
    for db in cursor.fetchall():
        strings.append(db)
    return strings

def ParseTime(database):
    tables = []
    cursor = cnx.cursor()
    execute_command = "SELECT `Дата создания` FROM " + database + ".`all configuration`;"
    cursor.execute(execute_command)
    for db in cursor.fetchall():
        for d in db:
            if d.day < 10:
                day = "0" + str(d.day)
            else:
                day = str(d.day)
            if d.month < 10:
                month = "0" + str(d.month)
            else:
                month = str(d.month)
            YMD = str(d.year) + "-" + month + "-" + day
            if YMD not in tables:
                tables.append(YMD)
    return tables

def ParseDB():
    disabled_databases = ['information_schema', 'mysql', 'performance_schema', 'sys']
    databases = []
    cursor = cnx.cursor()
    cursor.execute("Show databases;")
    for db in cursor.fetchall():
        for d in db:
            if d not in disabled_databases:
                databases.append(d)
    return databases
    
def Connect(MySQL_User, MySQL_Password, MySQL_Host, MySQL_Port):
    try:
        global cnx
        cnx = mysql.connector.connect(
            host=MySQL_Host,
            port=MySQL_Port,
            user=MySQL_User,
            password=MySQL_Password,
            auth_plugin='mysql_native_password',
            )
        print('Подключение к MYSQL произошло успешно')
        global cursor
        cursor = cnx.cursor()
        return 0
    except mysql.connector.errors.DatabaseError:
        print('Не удалось подключиться к MySQL')
        return 1001
    except mysql.connector.errors.InterfaceError:
        print('Не удалось подключиться к MySQL')
        return 1002