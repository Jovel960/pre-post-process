import sqlite3

sqLiteDB = None

def connectToDb():
    global sqLiteDB
    if sqLiteDB is None:
        conn = sqlite3.connect('db.sqlite3')
        # Create a cursor object using the cursor() method
        sqLiteDB = conn
    return sqLiteDB

def getDB():
    return sqLiteDB

def createQuery(query):
    # Execute the SQL query
    sqLiteDB.execute(query)
    # Fetch all rows of the query result
    return sqLiteDB.fetchall()

def closeConnection():
    # Close the connection
    sqLiteDB.close()