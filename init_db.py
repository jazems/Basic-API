import sqlite3
import uuid

newTaskId = uuid.uuid4()

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()