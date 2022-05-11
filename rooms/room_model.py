class Room:
    def __init__(self, id: int, owner_id: int, password: str):
        self.id = id
        self.owner_id = owner_id
        self.password = password