import cPickle
import MySQLdb


class Alix(object):
	def __init__(self):
		self.data = {'alix': 5}

## Create a semi-complex list to pickle
listToPickle = {'aLEX': 5}

listToPickle = Alix()

## Pickle the list into a string
pickledList = cPickle.dumps(listToPickle)

## Connect to the database as localhost, user pickle,
## password cucumber, database lists
connection = MySQLdb.connect('127.0.0.1', 'testuser', 'test123', 'testdb')

## Create a cursor for interacting
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Locu")
cursor.execute("CREATE TABLE Locu(Id INT PRIMARY KEY AUTO_INCREMENT,  card VARCHAR(25),  features BLOB)")

## Add the information to the database table pickleTest
cursor.execute("""INSERT INTO Locu VALUES (NULL, 'testCard', %s)""", (pickledList, ))

## Select what we just added
cursor.execute("""SELECT features FROM Locu WHERE card = 'testCard'""")

## Dump the results to a string
rows = cursor.fetchall()

## Get the results
for each in rows:
	## The result is also in a tuple
	for pickledStoredList in each:
		## Unpickle the stored string
		unpickledList = cPickle.loads(pickledStoredList)
		print unpickledList.data