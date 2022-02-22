import sqlite3
import uuid

newTaskId = uuid.uuid4()

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO tasks_3035705646 (title, is_completed) VALUES (?, ?)",
            ('Test_name', False)
            )

connection.commit()
connection.close()