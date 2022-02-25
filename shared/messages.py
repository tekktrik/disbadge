"""
`shared.messages`
====================================================

Base class for holding Discord messages

* Author(s): Alec Delaney

"""

try:
    from typing import Optional, Any, Dict
except ImportError:
    pass


# pylint: disable=too-few-public-methods
class CommandType:
    """Enum-like class for command types"""

    NONE = 0
    PING = 1
    CHEER = 2
    HYPE = 3


class DiscordMessageBase:
    """The base class for representing Discord messages

    :param str message: (Optional) The Discord message; default is None
    :param str user: (Optional) The sender of the message; defualt is None
    :param int cmd_type: (Optional) The slash command type used to send the
        message; default is CommandType.NONE
    """

    def __init__(
        self,
        message: Optional[str] = None,
        user: Optional[str] = None,
        cmd_type: int = CommandType.NONE,
    ) -> None:

        self._message = message
        self._user = user
        self._cmd_type = cmd_type

    def __repr__(self) -> str:
        return "{0}: {1}".format(self.user, self.message)

    def __str__(self) -> str:
        return str(self._message)

    def __eq__(self, other: Any) -> bool:
        if other is None or not isinstance(DiscordMessageBase): # TODO: can probably just use isinstance()
            return False
        
        if other._message == self._message and other._user == self._user:
            return True
        return False

    def __add__(self, other: str) -> "DiscordMessageBase":
        if isinstance(other, DiscordMessageBase):
            self._message += other._message
            return self
        if isinstance(other, str):
            self._message += other
            return self
        raise TypeError("Can only add strings or other Discord messages")

    def __contains__(self, value: str) -> bool:
        if isinstance(value, str):
            return value in self._message
        raise TypeError("Can only check messages for strings")

    @property
    def user(self) -> Optional[str]:
        """The user that sent the message, including the number after username"""
        return self._user

    @property
    def message(self) -> Optional[str]:
        """The message that was sent"""
        return self._message

    @property
    def username(self) -> Optional[str]:
        """The username of the person that sent the message"""
        return self._user[:-5] if self._user is not None else None

    @property
    def cmd_type(self) -> Optional[int]:
        """The slash command type used to send the message"""
        return self._cmd_type

    @cmd_type.setter
    def cmd_type(self, command: int) -> None:
        self._cmd_type = command

    def to_json(self) -> Dict[str, Any]:
        """Converts the message object into an equivalent dict, must be
        implemented in subclasses of DiscordMessageBase"""
        raise NotImplementedError("Must be defined in subclass")

    def from_json(self, dict_object: Dict[str, Any]) -> None:
        """Converts a dict into the equivalent DiscordMessageBase object,
        must be implemented in subclasses of DiscordMessageBase
        """
        raise NotImplementedError("Must be defined in subclass")
