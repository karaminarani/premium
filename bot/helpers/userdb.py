from __future__ import annotations

from config import Config


class UserDB:
    conf: Config = Config()

    def __init__(self):
        self.db = self.conf.ASYNC_PYMONGO['users']

    async def all(self) -> list[dict]:
        cursor = self.db.find({})
        return [document async for document in cursor]

    async def list(self) -> list[int]:
        users = await self.all()
        return [user['_id'] for user in users]

    async def get(self, user_id: int) -> dict | None:
        return await self.db.find_one({'_id': user_id})

    async def add(self, user_id: int) -> None:
        await self.db.insert_one({'_id': user_id})

    async def remove(self, user_id: int) -> None:
        await self.db.delete_one({'_id': user_id})
