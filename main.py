from __future__ import annotations

import asyncio
import os
import sys

import aiofiles
from pyrogram.errors import RPCError

from bot.client import Bot


async def main():
    Bot.log.info('Truncating log')
    await logtruncate()

    Bot.log.info('Starting client')
    await start()

    Bot.log.info('Initialize DATABASE_ID')
    await chdb()

    Bot.log.info('Initialize FSUB_IDS')
    await getfs()

    await rmsg('restart.txt')
    await rmsg('broadcast.txt')


def errhndlr(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RPCError as e:
            Bot.log.error(e)
            sys.exit(1)
    return wrapper


async def logtruncate():
    async with aiofiles.open('log.txt', 'r+') as w:
        await w.truncate(0)


@errhndlr
async def start():
    await Bot.start()
    Bot.log.info('Client started')


@errhndlr
async def chdb():
    hello_world = await Bot.send_message(
        Bot.conf.DATABASE_ID,
        'Hello World!',
    )
    await hello_world.delete(revoke=True)
    Bot.log.info('DATABASE: Passed')


@errhndlr
async def getfs():
    for index, chat_id in enumerate(Bot.conf.FSUB_IDS):
        url = (await Bot.get_chat(chat_id)).invite_link
        setattr(Bot, f'{index + 1}', url)
        Bot.log.info(f'FSUB_{index + 1} passed')


async def rmsg(filepath):
    if os.path.exists(filepath):
        async with aiofiles.open(filepath, mode='r') as r:
            cid, mid = [int(i) for i in (await r.read()).split()]
        await Bot.send_message(
            cid,
            'Restarted.',
            reply_to_message_id=mid,
        )
        os.remove(filepath)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    Bot.log.info('Bot has been deployed')
    Bot.loop.run_forever()
