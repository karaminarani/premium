from __future__ import annotations

from pyrogram.filters import command
from pyrogram.filters import private
from pyrogram.filters import user
from pyrogram.types import Message

from .helpers import helpers
from bot.client import Bot


@Bot.on_message(~command(Bot.cmd.cmds) & private & user(Bot.conf.ADMIN_IDS))
async def generate(c: Bot, m: Message):
    genmsg = await m.reply('...', quote=True)
    copied = await m.copy(c.conf.DATABASE_ID, disable_notification=True)
    encode = c.safe.encode(f'id-{copied.id * abs(c.conf.DATABASE_ID)}')
    urlstr = helpers.urlstring(encode)
    markup = helpers.urlmarkup(helpers.urlstring(urlstr, share=True))
    await genmsg.edit(urlstr, reply_markup=markup)
