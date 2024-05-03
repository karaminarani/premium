from __future__ import annotations

import asyncio
from contextlib import suppress

from pyrogram.errors import FloodWait
from pyrogram.errors import RPCError
from pyrogram.filters import command
from pyrogram.filters import user
from pyrogram.types import Message

from .helpers import helpers
from bot.client import Bot


@Bot.on_message(command(Bot.cmd.broadcast) & user(Bot.conf.ADMIN_IDS))
async def broadcast(c: Bot, m: Message):
    if not (bcmsg := m.reply_to_message):
        return await m.reply('Reply to message.', quote=True)
    msg = await m.reply('...', quote=True)

    helpers.write('broadcast.txt', m.chat.id, msg.id)

    users = c.db.list()
    admns = len(c.conf.ADMIN_IDS)
    total = len(users) - admns if len(users) > admns else 0
    done, fail = 0, 0

    async def progress(msg) -> Message:
        nonlocal done, fail, total
        with suppress(Exception):
            await msg.edit(f'Sent: {done}/{total} - Failed: {fail}')

    c.log.info('Broadcasting')
    for user in users:
        if user in c.conf.ADMIN_IDS:
            continue
        try:
            await helpers.copy(bcmsg, user)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            c.log.warning(f'Floodwait - Sleep: {e.value}s')
        except RPCError:
            c.db.remove(user)
            fail += 1
        if (done + fail) % 25 == 0:
            asyncio.create_task(progress(msg))
    await m.reply(f'Sent: {done} - Failed: {fail}', quote=True)
    c.log.info('Broadcast finished')
    return await msg.delete()
