import sqlite3, hashlib

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT)'''
)
conn.commit()

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

if len(rows) < 1:
    password = 'testuserps'
    hashObj = hashlib.sha256(password.encode())
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('test', hashObj.hexdigest()))
    conn.commit()

conn.close()

def checkauth(username, password):
    hashObj = hashlib.sha256(password.encode())

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashObj.hexdigest()))
    rows = cursor.fetchall()
    conn.close()
    return True if len(rows) > 0 else False
