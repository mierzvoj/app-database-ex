import sqlite3
import sqlite3
from sqlite3 import Cursor


class Database(object):
    def __int__(self):
        return self

    connection = sqlite3.connect("users.db", timeout=10)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()
    connection.isolation_level = ''
    print("database connected")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY,
            login text NOT NULL UNIQUE,
            password text NOT NULL
            )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id integer PRIMARY KEY,
            password text NOT NULL,
            owner_id integer NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_rooms (
            id integer PRIMARY KEY,
            room_id integer NOT NULL,
            user_id integer NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (room_id) REFERENCES rooms (id),
            UNIQUE(room_id, user_id)
           ) 
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id integer PRIMARY KEY,
            topic_id integer NOT NULL,
            user_id integer NOT NULL,
            vote float NOT NULL,
            FOREIGN KEY (topic_id ) REFERENCES topics (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE (user_id, topic_id)
                    ) 
                ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id integer PRIMARY KEY,
            room_id integer NOT NULL,
            subject text NOT NULL,
            FOREIGN KEY (room_id) references rooms (id)
            ) 
        ''')
