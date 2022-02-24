from typing import Dict, Any
from shared.messages import DiscordMessageBase

class RPiDiscordMessage(DiscordMessageBase):
    """The extension of DiscordMessage Base that is used by the
    Raspberry Pi"""

    def to_json(self) -> Dict[str, Any]:
        return {
            "message": self._message,
            "user": self._user,
            "cmd_type": self._cmd_type,
        }
