from __future__ import annotations

import os

from async_pymongo import AsyncClient
from dotenv import load_dotenv

load_dotenv('config.env')


class Config:
    API_ID = int(os.getenv('API_ID', 2040))
    API_HASH = os.getenv('API_HASH', 'b18441a1ff607e10a989891a5462e627')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    BOT_ID = BOT_TOKEN.split(':', 1)[0]
    OWNER_ID = int(os.getenv('OWNER_ID', 487936750))
    ADMIN_IDS = [int(i) for i in os.environ.get('ADMIN_IDS', '').split()]
    ADMIN_IDS.append(OWNER_ID)
    DATABASE_ID = int(os.getenv('DATABASE_ID'))
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://root:passwd@mongo')
    FSUB_IDS = [int(i) for i in os.environ.get('FSUB_IDS', '').split()]
    PROTECT_CONTENT = os.environ.get('PROTECT_CONTENT', 'True') == 'True'
    ASYNC_PYMONGO = AsyncClient(MONGO_URL)[BOT_ID]
