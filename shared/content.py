import json

try:
    from typing import Optional
except ImportError:
    pass

class CommandType:

    PING = 0
    CHEER = 1
    HYPE = 2

class DiscordMessageBase:

    def __init__(self, message: str, username: Optional[str] = None, cmd_type: Optional[int] = None) -> None:

        self.message = message
        self.username = username
        self.cmd_type = cmd_type

    def transmit(self):
        raise NotImplementedError("Must be defined in subclass")

    @classmethod
    def receive(cls, payload: str):
        raise NotImplementedError("Must be defined in subclass")
