"""Pickling the Menu data from locu query"""

from os.path import exists
import sys
import pickle
import MySQLdb
import cPickle


class MenuDatabase(object):
    def __init__(self):
        self.data = {}

    def save(self, file_name):
        if not exists(file_name):
            f = open(file_name, 'w')
        else:
            f = open(file_name, 'r+')
        f.seek(0, 0)
        pickle.dump(self, f)
        f.close()

        """
        print self.data
        pickled = cPickle.dumps(self.data)
        print pickled

        connection = MySQLdb.connect('127.0.0.1', 'testuser', 'test123', 'testdb')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS Locu")
        cursor.execute("CREATE TABLE Locu(Id INT PRIMARY KEY AUTO_INCREMENT,  card VARCHAR(25),  features BLOB)")
        cursor.execute("INSERT INTO Locu VALUES (NULL, 'testCard', %s)", (pickled, ))
        """

    def __str__(self):
        return str(self.data)


def load(file_name):
    if not exists(file_name):
        return MenuDatabase()
    else:
        f = open(file_name, 'r+')
        f.seek(0, 0)
        obj = pickle.load(f)
        f.close()
        return obj

    """

    connection = MySQLdb.connect('127.0.0.1', 'testuser', 'test123', 'testdb')
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES LIKE 'Locu'")
    result = cursor.fetchone()
    database = None
    if result:

        cursor.execute("SELECT features FROM Locu WHERE card = 'testCard'")
        rows = cursor.fetchall()
        print rows
        for each in rows:
            print 'UNPICKLED!!!'
            for pickled_database in each:
                unpickled = cPickle.loads(pickled_database)
                return unpickled
        return MenuDatabase()
    else:
        return MenuDatabase()
    """

