from __future__ import annotations

from pyrogram.filters import command
from pyrogram.filters import private
from pyrogram.filters import user
from pyrogram.types import Message

from .helpers import helpers
from bot.client import Bot


@Bot.on_message(command(Bot.cmd.batch) & private & user(Bot.conf.ADMIN_IDS))
async def batch(c: Bot, m: Message):
    chat_id = m.chat.id
    user_id = m.from_user.id

    def encoder(first: int, last: int) -> str:
        _data = first * abs(c.conf.DATABASE_ID)
        data_ = last * abs(c.conf.DATABASE_ID)
        return c.safe.encode(f'id-{_data}-{data_}')

    fask = await c.ask(
        chat_id=chat_id,
        text='Forward: First Message',
        user_id=user_id,
    )
    if (
        not fask.forward_from_chat
        or not fask.forward_from_chat.id == c.conf.DATABASE_ID
    ):
        return await fask.reply('Invalid', quote=True)
    first = fask.forward_from_message_id
    while True:
        lask = await c.ask(
            chat_id=chat_id,
            text='Forward: Last Message',
            user_id=user_id,
        )
        if (
            not lask.forward_from_chat 
            or not lask.forward_from_chat.id == c.conf.DATABASE_ID
        ):
            return await lask.reply('Invalid', quote=True)
        last = lask.forward_from_message_id
        break
    if (abs(int(last) - int(first)) + 1) > 200:
        return await m.reply("Can't retrieve >200 messages.")
    encode = encoder(first, last)
    urlstr = helpers.urlstring(encode)
    markup = helpers.urlmarkup(helpers.urlstring(urlstr, share=True))
    await m.reply(urlstr, quote=True, reply_markup=markup)
