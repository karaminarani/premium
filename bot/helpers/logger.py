from __future__ import annotations

import datetime
import logging


class Time:
    def __init__(self, offset):
        self.offset = offset

    def _offset_(self):
        utctime = datetime.datetime.utcnow()
        timeoffset = datetime.timedelta(hours=self.offset)
        return utctime + timeoffset

    def converted(self, *args):
        return self._offset_().timetuple()


class Logger:
    logtime: Time = Time(7)
    logfile = 'log.txt'
    logformat = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

    def __init__(self):
        self.setup_logger()

    def setup_logger(self):
        logging.Formatter.converter = self.logtime.converted
        logging.basicConfig(
            format=self.logformat,
            datefmt='%x %X',
            handlers=[
                logging.FileHandler(
                    self.logfile,
                ), logging.StreamHandler(),
            ],
            level=logging.INFO,
        )
        logging.getLogger('pyrogram').setLevel(logging.ERROR)
        self.log = logging.getLogger('Bot')


Logger = Logger()
