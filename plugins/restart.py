from __future__ import annotations

import subprocess

from pyrogram.filters import command
from pyrogram.filters import private
from pyrogram.filters import user
from pyrogram.types import Message

from .helpers import helpers
from bot.client import Bot


@Bot.on_message(command(Bot.cmd.restart) & private & user(Bot.conf.OWNER_ID))
async def restart(c: Bot, m: Message):
    msg = await m.reply('Restarting...', quote=True)
    helpers.write('restart.txt', m.chat.id, msg.id)
    subprocess.run(['python', 'main.py'])
