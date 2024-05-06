from __future__ import annotations

import aiofiles
from pyrogram.errors import RPCError
from pyrogram.helpers import ikb
from pyrogram.types import Message

from bot.client import Bot


class Helpers:
    greeting: str = 'The bot is up and running. '\
                    'These bots can store messages in custom chats, '\
                    'and users access them through the bot.'
    forcemsg: str = 'To view messages shared by bots. '\
                    'Join first, then press the Try Again button.'
    bttnrows: int = 3

    def __init__(self, client: callable):
        self.c = client

    def urlmarkup(self, url: str) -> ikb:
        return ikb([[('Share', url, 'url')]])

    def urlstring(self, string: str, share=False) -> str:
        if share:
            return f'https://t.me/share/url?url={string}'
        return f'https://t.me/{self.c.me.username}?start={string}'

    def buttons(self, m: callable[Message]) -> None:
        if not self.c.conf.FSUB_IDS:
            return None
        buttons = [
            [
                (f'Join {index + 1}', getattr(self.c, f'{index + 1}'), 'url')
                for index in range(
                    start,
                    min(
                        start + self.bttnrows,
                        len(self.c.conf.FSUB_IDS),
                    ),
                )
            ]
            for start in range(
                0,
                len(self.c.conf.FSUB_IDS),
                self.bttnrows,
            )
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

    async def copy(
        self,
        msg: callable[Message],
        _id: int,
    ) -> Message:
        await msg.copy(_id, protect_content=Bot.conf.PROTECT_CONTENT)

    async def write(
        self,
        file: str,
        cid: callable | int,
        mid: callable | int,
    ) -> None:
        async with aiofiles.open(file, 'w') as w:
            await w.write(f'{cid}\n{mid}')


helpers = Helpers(Bot)
