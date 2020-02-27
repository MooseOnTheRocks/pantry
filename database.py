# dbtest.py

import mysql.connector as mysql
from mysql.connector.errorcode import *

class DatabaseConnection:
    def __init__(self, host, user, password, database, **kwargs):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.kwargs = kwargs
    
    # -- SQL Support
    def select(self, table, *cols):
        if len(cols) == 0:
            return Cursor(self._connection, f"SELECT * FROM {table}")
        else:
            return Cursor(self._connection, f"SELECT {','.join(map(str, cols))} FROM {table}")
    
    def executeSQL(self, sql):
        return Cusor(self._connection, sql)
    
    def connect(self):
        self._connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, **self.kwargs)
        return self
    
    def close(self):
        if isinstance(type, mysql.Error):
            if value.errno == ER_ACCESS_DENIED_ERROR:
                print("Database access denied: bad username or password.")
            elif value.errno == ER_BAD_DB_ERROR:
                print("Could not connect to database; make sure you are connected to the OSU network.")
        self._connection.close()
        print("Closed db connection.")
    
    # -- Context Manager
    def __enter__(self):
        return connect
    
    def __exit__(self, type, value, traceback):
        self.close()

class Cursor:
    def __init__(self, connection, sql):
        self._connection = connection
        self._sql = sql
    
    def execute(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute(self._sql)
        return self
    
    def close(self):
        self._cursor.close()
    
    # -- Iterable
    def __iter__(self):
        return self._cursor
    
    # -- Context Manager
    def __enter__(self):
        return self.execute()
    
    def __exit__(self, type, value, traceback):
        self.close()

def connect(host, user, password, database, **kwargs):
    return DatabaseConnection(host, user, password, database, **kwargs).connect()