import json

try:
    from typing import Optional, Any
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

    def __repr__(self) -> str:
        return "{0}: {1}".format(self.username, self.message)

    def __str__(self) -> str:
        return str(self.message)

    def __eq__(self, __o: Any) -> bool:
        if isinstance(__o, DiscordMessageBase):
            if __o.message == self.message and __o.username == self.username:
                return True
            return False
        raise ValueError("Can only compare to other Discord messages")

    def transmit(self):
        raise NotImplementedError("Must be defined in subclass")

    @classmethod
    def receive(cls, payload: str):
        raise NotImplementedError("Must be defined in subclass")
