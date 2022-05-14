class Room:
    def __init__(self, room_id: int, owner_id: int, password: str):
        self.room_id = room_id
        self.owner_id = owner_id
        self.password = password