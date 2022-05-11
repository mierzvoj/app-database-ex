import sqlite3
from sqlite3 import Cursor
from typing import List

import bcrypt

from database.database import Database
from users.user_model import User


def insertIntoUsers(db: Cursor, login: str, password: str):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(f'INSERT OR IGNORE INTO users(login, password) VALUES(\"{login}\", \"{password}\")')
    conn.commit()
    conn.close()


def ifUserExists(db: Cursor, login: str):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    return len(cur.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchall()) > 0


def login(db: Cursor, login: str, password: str):
    conn = sqlite3.connect("users.db")
    user = conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()
    if user is None:
        return None
    if not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return None
    return User(id=user[0], login=user[1])


def getAllUsers(db: Cursor) -> List[User]:
    return [User(id=user[0], login=user[1]) for user in db.execute("SELECT * FROM users")]


def deleteUser(db: Cursor, login):
    db.execute("DELETE FROM users WHERE login = ?", (login,))
