import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT NOT NULL,
          password TEXT NOT NULL,
          result TEXT NOT NULL
    )
          ''')
c.execute('INSERT INTO users (username, password) VALUES (?,?)',('users1','password1'))
c.execute('INSERT INTO users (username, password) VALUES (?,?)',('users2','password2'))

conn.commit()
conn.close()
