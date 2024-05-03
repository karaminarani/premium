from __future__ import annotations

import time

from pyrogram.filters import command
from pyrogram.filters import private
from pyrogram.filters import user
from pyrogram.types import Message

from bot.client import Bot


@Bot.on_message(command(Bot.cmd.ping) & private)
async def ping(_, m: Message):
    _ping = time.time()
    ping = await m.reply('...', quote=True)
    ping_ = (time.time() - _ping) * 1000
    return await ping.edit(f'{ping_:.2f} ms')


@Bot.on_message(command(Bot.cmd.users) & private & user(Bot.conf.ADMIN_IDS))
async def users(c: Bot, m: Message):
    users = c.db.list()
    await m.reply(f'{len(users)} users', quote=True)
