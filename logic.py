import sqlite3


class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def add_owner(self, user_id, user_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.execute(
                'INSERT INTO owner (id, name) VALUES (?, ?) ON CONFLICT(id) DO NOTHING',
                (user_id, user_name)
            )
            conn.commit()
        conn.close()
        return cursor.rowcount > 0

    def get_owner(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            owner = conn.execute(
                'SELECT id, name FROM owner WHERE id = ?', (user_id,)
            ).fetchone()
        conn.close()
        return owner

    def get_statuses(self):
        conn = sqlite3.connect(self.database)
        with conn:
            statuses = conn.execute('SELECT name FROM status ORDER BY id').fetchall()
        conn.close()
        return [row[0] for row in statuses]

    def get_tasks(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            tasks = conn.execute('''
                SELECT task.id, task.name, status.name
                FROM task JOIN status ON task.status_id = status.id
                WHERE task.owner_id = ? ORDER BY task.id
            ''', (user_id,)).fetchall()
        conn.close()
        return tasks

    def add_task(self, user_id, task_name):
        if not self.get_owner(user_id):
            return False
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.execute('''
                INSERT INTO task (name, owner_id, status_id)
                SELECT ?, ?, id FROM status WHERE name = 'todo'
            ''', (task_name, user_id))
            conn.commit()
        conn.close()
        return cursor.rowcount > 0

    def update_task(self, user_id, task_id, status_name):
        if status_name not in self.get_statuses():
            return False
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.execute('''
                UPDATE task SET status_id = (SELECT id FROM status WHERE name = ?)
                WHERE id = ? AND owner_id = ?
            ''', (status_name, task_id, user_id))
            conn.commit()
        conn.close()
        return cursor.rowcount > 0

    def delete_task(self, user_id, task_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.execute(
                'DELETE FROM task WHERE id = ? AND owner_id = ?', (task_id, user_id)
            )
            conn.commit()
        conn.close()
        return cursor.rowcount > 0
