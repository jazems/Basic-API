import sqlite3
from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/v1/tasks', methods=['GET', 'POST'])
def index():
    conn = get_connection()
    task = request.get_json()

    if request.method == 'POST':
        try:
            title = task['title']

            if 'is_completed' in task:
                is_completed = task['is_completed']
            else:
                is_completed = False
    
            cur = conn.cursor()

            cur.execute('INSERT INTO tasks_3035705646 (title, is_completed) VALUES (?, ?)',
            (title, is_completed)
            )

            conn.commit()
            id = cur.lastrowid
            conn.close()
            return {'id': id}
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400

    else:
        tasks = conn.execute('SELECT * FROM tasks_3035705646').fetchall()
        conn.close()
        taskList = []
        for task in list(tasks):
            taskList.append({
            'task_id': task['task_id'],
            'title': task['title'],
            'is_completed': task['is_completed']})
        return {'data': taskList}, 200

@app.route('/v1/tasks/<id>', methods=['GET', 'DELETE', 'PUT'])
def id(id):
    
    conn = get_connection()
    cur = conn.cursor()
    updated = request.get_json()

    if request.method == 'GET':
        task = cur.execute('SELECT * FROM tasks_3035705646 WHERE task_id = (?)',
        id
        ).fetchone()

        conn.commit()
        conn.close()

        return {'id': task['task_id'], 'title': task['title'], 'is_completed': task['is_completed']}
    elif request.method == 'DELETE':
        cur.execute('DELETE FROM tasks_3035705646 WHERE task_id = (?)',
        id
        )

        conn.commit()
        conn.close()

        return ('', 200)
    else:
        title, is_completed = updated['title'], updated['is_completed']

        cur.execute('UPDATE tasks_3035705646 SET title = (?) WHERE task_id = (?)',
        (title, id)
        )

        cur.execute('UPDATE tasks_3035705646 SET is_completed = (?) WHERE task_id = (?)',
        (is_completed, id)
        )

        conn.commit()
        conn.close()

        return ('', 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

