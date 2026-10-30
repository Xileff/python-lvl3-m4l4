import sqlite3

class DbManager:
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

  def get_tasks(self, user_id):
    conn = sqlite3.connect(self.database)
    with conn:
      tasks = conn.execute('''
        SELECT task.id, task.name, status.name
        FROM task JOIN status ON task.status_id = status.id
        WHERE task.owner_id = ?
        ORDER BY task.id
      ''', (user_id)).fetchall()
    conn.close()
    return tasks

  def add_task(self, user_id, task_name):
      conn = sqlite3.connect(self.database)
      with conn:
        cursor = conn.execute(
          'INSERT INTO task (name, status_id, owner_id) VALUES (?, ?, ?)',
          (task_name, 1, user_id)
        )
        conn.commit()
      conn.close()
      return cursor.rowcount > 0

  def update_task(self, user_id, task_id, status_id):
    conn = sqlite3.connect(self.database)
    with conn:
      cursor = conn.execute(
        '''
          UPDATE task SET status_id = ?
          WHERE id = ? AND owner_id = ?
        ''',
        (status_id, task_id, user_id)
      )
      conn.commit()
    conn.close()
    return cursor.rowcount > 0

  def delete_task(self, user_id, task_id):
    conn = sqlite3.connect(self.database)
    with conn:
      cursor = conn.execute(
        'DELETE FROM task WHERE id = ? AND owner_id = ?',
        (task_id, user_id)
      )
      conn.commit()
    conn.close()
    return cursor.rowcount > 0
