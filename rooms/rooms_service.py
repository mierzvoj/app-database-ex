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
    connection.execute(f'INSERT OR IGNORE INTO rooms(password, owner_id) VALUES(\"{password}\", \"{owner_id}\")')
    connection.commit()
    connection.close()
    print("Room added successfully")


def findRoomById(db: Cursor, id: int):
    room = connection.execute('''SELECT * FROM rooms WHERE id = ?''', (id,)).fetchone()
    return Room(id=room[0], password=room[1], owner_id=room[2])



def deleteRoomById(db: Cursor, id: int):
    connection.execute("DELETE FROM joined_rooms WHERE id=?", (id,))
    connection.execute("DELETE FROM rooms WHERE id=?", (id,))
    connection.commit()
    connection.close()


def joinRoom(db: Cursor, user_id: int, room_id: int, password: str) -> bool:
    room = findRoomById(db, room_id)
    if room is None:
        return False

    if not bcrypt.checkpw(password.encode('utf-8'), room.password.encode('utf-8')):
        return False

    connection.execute("INSERT INTO joined_rooms (user_id, room_id) VALUES (?, ?)", (user_id, room_id))
    return True
