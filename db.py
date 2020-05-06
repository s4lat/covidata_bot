import sqlite3, datetime

class DB:
	def __init__(self, db_path):
		self.db_path = db_path

	def create_user(self, user):
		conn = sqlite3.connect(self.db_path)

		with conn:
			c = conn.cursor()

			c.execute("SELECT * FROM users WHERE id=? LIMIT 1;", (user['id'], ))
			is_exist = c.fetchone()

			if not is_exist:
				c.execute('''INSERT INTO users ("id", "username", "lang_code", "last_seen")
					VALUES (?, ?, ?, ?);''', (user['id'], user['username'], 
						user['language_code'], datetime.datetime.now()))

		if is_exist:
			self.update_user(user)


	def update_user(self, user):
		conn = sqlite3.connect(self.db_path)

		with conn:
			c = conn.cursor()
			c.execute('''UPDATE users 
						 SET last_seen = ? 
						 WHERE id = ?
				''', (datetime.datetime.now(), user['id']))

		pass

