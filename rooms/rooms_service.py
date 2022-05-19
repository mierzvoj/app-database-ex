import sqlite3
from sqlite3 import Cursor
from typing import List, Union
import bcrypt

from database.database import Database
from rooms.room_model import Room
from rooms.topics_model import Topic

connection = sqlite3.connect("users.db", timeout=10)


def insertIntoRooms(db: Cursor, owner_id: str, password: str):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    connection.execute(f'INSERT OR IGNORE INTO rooms(password, owner_id) VALUES(\"{password}\", \"{owner_id}\")')
    connection.commit()
    connection.close()
    print("Room added successfully")


def findRoomById(db: Cursor, id):
    room = connection.execute('''SELECT * FROM rooms WHERE id = ?''', (id,)).fetchone()
    return Room(room_id=room[0], password=room[1], owner_id=room[2])


def deleteRoomById(db: Cursor, id):
    # connection.execute("DELETE FROM joined_rooms WHERE id=?", (id,))
    connection.execute('''DELETE FROM rooms WHERE id = ?''', (id,))
    connection.execute('''DELETE FROM users_rooms WHERE id = ?''', (id,))
    connection.commit()
    connection.close()


def joinRoom(db: Cursor, user_id: int, room_id: int, password: str) -> bool:
    room = findRoomById(db, room_id)
    if room is None:
        return False
    if not bcrypt.checkpw(password.encode('utf-8'), room.password.encode('utf-8')):
        return False
    connection.execute("INSERT INTO users_rooms (user_id, room_id) VALUES (?, ?)", (user_id, room_id))
    connection.commit()
    connection.close()
    print('Joined succesfully')
    return True


def createTopic(db: Cursor, room_id: int, topic: str):
    connection.execute("INSERT INTO topics (room_id, subject) VALUES (?, ?)", (room_id, topic))
    connection.commit()
    connection.close()
    print('Topic created succesfully')


def addVote(db: Cursor, topic_id: int, vote: float, user_id: int):
    connection.execute("INSERT INTO votes (topic_id, vote, user_id) VALUES (?, ?, ?)", (topic_id, vote, user_id))
    connection.commit()
    connection.close()


def getTopic(db: Cursor, room_id: int) -> Union[Topic, None]:
    topic = db.execute("SELECT * FROM topics WHERE room_id = ?", (room_id, )).fetchone()
    if topic is None:
        return None

    return Topic(id=topic[0], room_id=topic[1], subject=topic[2])


def getTopicById(db: Cursor, topic_id: int) -> Union[Topic, None]:
    topic = db.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
    if topic is None:
        return None
    return Topic(id=topic[0], room_id=topic[1], subject=topic[2])


def joinedRoom(db: Cursor, user_id: int, room_id: int) -> bool:
    return len(connection.execute("SELECT * FROM joined_rooms WHERE room_id = ? AND user_id = ?", (room_id, user_id)).fetchall()) > 0


def deleteTopic(db: Cursor, room_id: int):
    db.execute("DELETE FROM topics WHERE room_id = ?", (room_id, ))


def deleteVotes(db: Cursor, topic_id: int):
        db.execute("DELETE FROM votes WHERE topic_id=?", (topic_id,))