from __future__ import annotations

import base64


class URLSafe:
    @staticmethod
    def addpad(data: str) -> str:
        return data + '=' * (-len(data) % 4)

    @staticmethod
    def delpad(data: str) -> str:
        return data.rstrip('=')

    def encode(self, data: str) -> str:
        encoded = base64.urlsafe_b64encode(data.encode('utf-8'))
        return self.delpad(encoded.decode('utf-8'))

    def decode(self, data: str) -> str:
        padded = self.addpad(data)
        decoded = base64.urlsafe_b64decode(padded)
        return decoded.decode('utf-8')


class BotCommands:
    cmds: cmds = []

    def __init__(self):
        self.start = 'start'
        self.batch = 'batch'
        self.broadcast = 'broadcast'
        self.ping = 'ping'
        self.users = 'users'
        self.log = 'log'
        self.restart = 'restart'
        for attr, value in vars(self).items():
            self.cmds.append(value)
