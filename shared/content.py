import json

try:
    from typing import Optional
except ImportError:
    pass

class DiscordMessage:

    def __init__(self, message: str, username: Optional[str] = None) -> None:

        self.message = message
        self.username = username

    def transmit(self):
        raise NotImplementedError("Must be defined in subclass")

    @classmethod
    def receive(cls, payload: str):
        raise NotImplementedError("Must be defined in subclass")
