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

    def __init__(self, message: str, user: Optional[str] = None, cmd_type: Optional[int] = None) -> None:

        self._message = message
        self._user = user
        self._cmd_type = cmd_type

    def __repr__(self) -> str:
        return "{0}: {1}".format(self.user, self.message)

    def __str__(self) -> str:
        return str(self._message)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DiscordMessageBase):
            if other._message == self._message and other._user == self._user:
                return True
            return False
        raise TypeError("Can only compare to other Discord messages")

    def __contains__(self, value: str) -> bool:
        if isinstance(value, str):
            return value in self._message
        raise TypeError("Can only check messages for strings")

    @property
    def user(self) -> str:
        return self._user

    @property
    def message(self) -> str:
        return self._message

    @property
    def command_type(self) -> int:
        return self._cmd_type

    @property
    def username(self) -> str:
        return self._user[:-5]

    def to_payload(self) -> str:
        raise NotImplementedError("Must be defined in subclass")

    @classmethod
    def from_payload(cls, payload: str) -> "DiscordMessageBase":
        raise NotImplementedError("Must be defined in subclass")
