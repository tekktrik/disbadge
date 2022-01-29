from typing import Dict, Any
from shared.messages import DiscordMessageBase

class RPiDiscordMessage(DiscordMessageBase):
    """The extension of DiscordMessage Base that is used by the
    Raspberry Pi"""

    def to_dict(self) -> Dict[str, Any]:
        dict_object = {
            "message": self._message,
            "user": self._user,
            "cmd_type": self._cmd_type,
        }
        return dict_object
