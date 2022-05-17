import sqlite3
from sqlite3 import Cursor
from typing import List
import bcrypt

from database.database import Database
from rooms.room_model import Room
connection = sqlite3.connect("users.db", timeout=10)

def insertIntoRooms(db: Cursor, owner_id: str, password: str):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    db.execute(f'INSERT OR IGNORE INTO rooms(owner_id, password) VALUES(\"{owner_id}\", \"{password}\")')
    connection.commit()
    connection.close()
    print("Room added successfully")


def findRoomById(db: Cursor, room_id: int):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    return len(cur.execute("SELECT * FROM rooms WHERE room_id = ?", (room_id,)).fetchone())
    conn.close()
