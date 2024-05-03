from __future__ import annotations

from pyrogram.filters import command
from pyrogram.filters import private
from pyrogram.filters import user
from pyrogram.types import Message

from bot.client import Bot


@Bot.on_message(command(Bot.cmd.log) & private & user(Bot.conf.OWNER_ID))
async def log(c: Bot, m: Message):
    await m.reply_document('log.txt', quote=True)
