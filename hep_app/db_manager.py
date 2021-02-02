import sqlite3 as sq

def create_usertable():
    with sq.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS userstable(username Text,password TEXT)')


def add_userdata(username, password):
    with sq.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        conn.commit()


def login_user(username,password):
    with sq.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM userstable WHERE username=? AND password=?',(username,password))
        data = c.fetchall()
        return data

def view_all_users():
    with sq.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
    return data