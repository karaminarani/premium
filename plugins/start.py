from __future__ import annotations

import asyncio

from pyrogram.errors import FloodWait
from pyrogram.errors import RPCError
from pyrogram.filters import command
from pyrogram.filters import private
from pyrogram.types import Message

from .helpers import helpers
from bot.client import Bot


@Bot.on_message(command(Bot.cmd.start) & private)
async def start(c: Bot, m: Message):
    user = m.from_user.id
    if not c.db.get(user):
        c.db.add(user)
    if len(m.command) == 1:
        return await m.reply(
            helpers.greeting,
            quote=True,
            reply_markup=helpers.buttons(m),
        )
    if not await helpers.joined(user):
        return await m.reply(
            helpers.forcemsg,
            quote=True,
            reply_markup=helpers.buttons(m),
        )
    msgids = []
    decode = c.safe.decode(m.command[1]).split('-')
    _msgid = int(int(decode[1]) / abs(c.conf.DATABASE_ID))
    if len(decode) == 2:
        msgids.append(_msgid)
    elif len(decode) == 3:
        msgid_ = int(int(decode[2]) / abs(c.conf.DATABASE_ID))
        msgids = range(
            _msgid, msgid_ +
            1,
        ) if _msgid < msgid_ else range(_msgid, msgid_ - 1, -1)
    msgs = await c.get_messages(c.conf.DATABASE_ID, msgids)
    for msg in msgs:
        try:
            await helpers.copy(msg, user)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            c.log.warning(f'Floodwait - Sleep: {e.value}s')
        except RPCError:
            continue
