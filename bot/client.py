from __future__ import annotations

import uvloop
from pyromod import Client

from .helpers.logger import Logger
from .helpers.misc import BotCommands
from .helpers.misc import URLSafe
from .helpers.userdb import UserDB
from config import Config


class Bot(Client):
    db: UserDB = UserDB()
    cmd: BotCommands = BotCommands()
    log: Logger = Logger.log
    safe: URLSafe = URLSafe()
    conf: Config = Config()

    def __init__(self, **kwargs):
        self.args = kwargs

        name = self.__class__.__name__.title()
        api_id = self.conf.API_ID
        api_hash = self.conf.API_HASH
        bot_token = self.conf.BOT_TOKEN

        super().__init__(
            name, api_id, api_hash,
            bot_token=bot_token,
            **kwargs,
        )

    async def start(self):
        uvloop.install()
        await super().start()

    async def stop(self, *args):
        await super().stop()


Bot = Bot(in_memory=True, plugins=dict(root='plugins'))
