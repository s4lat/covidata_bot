import sqlite3

conn = sqlite3.connect('db.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users 
    (id integer primary key, 
    username text NOT NULL, 
    lang_code text NOT NULL, 
    last_seen timestamp)''')

c.close()

# datetime.datetime.now()
