import sqlite3

class  LeaderTop:
    def __init__(self):
        connection = sqlite3.connect('leaders_top.db')
        cursor = connection.cursor()
        cursor.execute('''
                                       CREATE TABLE IF NOT EXISTS Users (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       username TEXT DEFAULT '',
                                       score INTEGER DEFAULT 0
                                       )
                                       ''')
        connection.commit()
        connection.close()

    def insert_nickname(self, username):
        connection = sqlite3.connect('leaders_top.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Users (username) VALUES (?)
            ''', (username,))
        connection.commit()
        connection.close()

    def update_score(self, score, username):
        connection = sqlite3.connect('leaders_top.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE Users SET score = ? WHERE username = ? AND score < ?',
                       (score, username, score))
        connection.commit()
        connection.close()

    def get_top(self)->list:
        connection = sqlite3.connect('leaders_top.db')
        cursor = connection.cursor()
        cursor.execute('SELECT username, score FROM Users ORDER BY score DESC')
        results = cursor.fetchall()
        connection.close()
        return results