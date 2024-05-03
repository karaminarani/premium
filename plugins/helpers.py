from __future__ import annotations

from pyrogram.errors import RPCError
from pyrogram.types import Message
from pyromod.helpers import ikb

from bot.client import Bot


class Helpers:
    greeting = 'The bot is up and running. '\
               'These bots can store messages in custom chats, '\
               'and users access them through the bot.'
    forcemsg = 'To view messages shared by bots. '\
               'Join first, then press the Try Again button.'

    def __init__(self, Bot):
        self.c = Bot

    def urlmarkup(self, url) -> ikb:
        return ikb([[('Share', url, 'url')]])

    def urlstring(self, string, share=False) -> str:
        if share:
            return f'https://t.me/share/url?url={string}'
        return f'https://t.me/{self.c.me.username}?start={string}'

    def buttons(self, m) -> None:
        if not self.c.conf.FSUB_IDS:
            return None
        buttons = [
            [
                (f'Join {index + 1}', getattr(self.c, f'{index + 1}'), 'url')
                for index in range(
                    start, min(
                        start + 3, len(self.c.conf.FSUB_IDS),
                    ),
                )
            ]
            for start in range(0, len(self.c.conf.FSUB_IDS), 3)
        ]
        if len(m.command) > 1:
            buttons.append(
                [
                    ('Try Again', self.urlstring(m.command[1]), 'url'),
                ],
            )
        return ikb(buttons)

    async def joined(self, user: int) -> bool:
        if not self.c.conf.FSUB_IDS or user in self.c.conf.ADMIN_IDS:
            return True
        for chat_id in self.c.conf.FSUB_IDS:
            try:
                await self.c.get_chat_member(chat_id, user)
            except RPCError:
                return False
        return True

    async def copy(self, msg, _id: int) -> Message:
        await msg.copy(_id, protect_content=Bot.conf.PROTECT_CONTENT)

    def write(self, file, cid: int, mid: int) -> Message:
        with open(file, 'w') as w:
            w.write(f'{cid}\n{mid}')


helpers = Helpers(Bot)
