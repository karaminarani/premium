from __future__ import annotations

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from config import Config


class UserDB:
    def __init__(self):
        self.conf: Config = Config()
        self.cli: MongoClient = MongoClient(self.conf.MONGO_URL)
        self.db: Database = self.cli[self.conf.MONGO_DB]
        self.users: Collection = self.db['users']

    def all(self) -> list[dict]:
        return list(self.users.find({}))

    def list(self) -> list[int]:
        return [user['_id'] for user in self.all()]

    def get(self, user_id: int) -> dict | None:
        return self.users.find_one({'_id': user_id})

    def add(self, user_id: int) -> None:
        self.users.insert_one({'_id': user_id})

    def remove(self, user_id: int) -> None:
        self.users.delete_one({'_id': user_id})
