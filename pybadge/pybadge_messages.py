import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import shared.layout as layout
import shared.messages as messages

try:
    from typing import Dict, Any
except ImportError:
    pass

# Load the title font
TITLE_FONTNAME = "/fonts/cherry-13-b.bdf"
TITLE_FONT = bitmap_font.load_font(TITLE_FONTNAME)

# Load the message font
MESSAGE_FONTNAME = "/fonts/cherry-11-r.bdf"
MESSAGE_FONT = bitmap_font.load_font(MESSAGE_FONTNAME)

class DiscordMessageGroup(displayio.Group, messages.DiscordMessageBase):
    """Display class for Discord messages"""

    max_lines = 5

    def __init__(self, message: str = "", user: str = "", cmd_type: int = messages.CommandType.NONE, dark_mode: bool = True) -> None:

        super().__init__()

        self._text_color = 0xFFFFFF if dark_mode else 0x000000
        self._message_label = None
        self._username_label = None
        self._cmd_type = cmd_type

        self.user = user
        self.message = message

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, name: str) -> None:

        if self._username_label:
            self.remove(self._username_label)

        self._username_label = Label(TITLE_FONT, text=name, color=self._text_color, y=8)
        self.append(self._username_label)
        self._message_label = None


    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, text: str) -> None:

        if self._message_label:
            self.remove(self._message_label)

        message_lines = layout.wrap_text(text, 26)
        self._wrapped_message = "\n".join(message_lines[:self.max_lines])

        self._message_label = Label(MESSAGE_FONT, text=self._wrapped_message, color=self._text_color, y=32)
        self.append(self._message_label)

    def from_payload(self, payload: Dict[str, Any]) -> "DiscordMessageGroup":
        
        self.message = payload["message"]
        self.user = payload["user"]
        self.cmd_type = payload["Cmd_type"]
