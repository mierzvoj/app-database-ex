import sqlite3
import sqlite3 as mdb
from sqlite3 import Cursor


class Database:
    def __int__(self):
        connectToDb()
        self.db = mdb.connect("users.db")
        self.cursor = self.db.cursor()

    def __enter__(self):
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        return self.connection, self.cursor

    def __exit__(self):
        pass

def connectToDb() -> sqlite3.Connection:
    db = mdb.connect("users.db")
    db.execute("pragma foreign_keys")
    createTableUsersRooms(db)
    createTableTasks(db)
    createTableUsers(db)
    createTablePoll(db)
    createTableUsersRooms(db)
    print("tables created")
    return db


def chk_conn(self):
    try:
        self.cursor()
        return True
    except Exception as ex:
        return False


myconn = mdb.connect("users.db")
if chk_conn(myconn):
    print("Database connected")
else:
    print("Database connection failed")


def createTableUsers(db: mdb.Connection):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id integer PRIMARY KEY,
            login text NOT NULL UNIQUE,
            password text NOT NULL
            )
        ''')


def createTableRooms(db: mdb.Connection):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_id integer PRIMARY KEY,
            password text NOT NULL,
            owner_id integer NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')


def createTableUsersRooms(db: mdb.Connection):
    cursor = db.cursor()
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


def createTablePoll(db: mdb.Connection):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS poll (
            id integer PRIMARY KEY,
            subject_id integer NOT NULL,
            task_id integer NOT NULL,
            user_id integer NOT NULL,
            vote float NOT NULL,
            FOREIGN KEY (task_id) REFERENCES tasks (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
                    ) 
                ''')


def createTableTasks(db: mdb.Connection):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id integer PRIMARY KEY,
            room_id integer NOT NULL,
            subject text NOT NULL,
            FOREIGN KEY (room_id) references rooms (id)
            ) 
        ''')
