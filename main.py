from __future__ import annotations

import asyncio
import os
import sys

import aiofiles
from pyrogram.errors import RPCError

from bot.client import Bot


async def main():
    Bot.log.info('Truncating log')
    logtruncate()

    Bot.log.info('Starting client')
    await start()

    Bot.log.info('Initialize FSUB_IDS')
    await getfs()

    await rmsg('restart.txt')
    await rmsg('broadcast.txt')


def logtruncate():
    with open('log.txt', 'r+') as w:
        w.truncate(0)


async def start():
    try:
        await Bot.start()
        Bot.log.info('Client started')
    except RPCError as e:
        Bot.log.info(e)
        sys.exit(1)


async def getfs():
    for index, chat_id in enumerate(Bot.conf.FSUB_IDS):
        try:
            url = (await Bot.get_chat(chat_id)).invite_link
            setattr(Bot, f'{index + 1}', url)
            Bot.log.info(f'FSUB_{index + 1} passed')
        except RPCError as e:
            Bot.log.error(f'FSUB_{index + 1}: {e}')
            sys.exit(1)


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
