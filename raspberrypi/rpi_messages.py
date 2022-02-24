from typing import Dict, Any
from shared.messages import DiscordMessageBase
from shared.uri_codec import encode_characters

class RPiDiscordMessage(DiscordMessageBase):
    """The extension of DiscordMessage Base that is used by the
    Raspberry Pi"""

    def to_json(self) -> Dict[str, Any]:
        return {
            "message": encode_characters(self._message),
            "user": encode_characters(self._user),
            "cmdtype": encode_characters(self._cmd_type),
        }
