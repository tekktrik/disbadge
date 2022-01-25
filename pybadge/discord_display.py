import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import shared.layout_helper as layout
import shared.messages as messages

# Load the title font
TITLE_FONTNAME = "/fonts/cherry-13-b.bdf"
TITLE_FONT = bitmap_font.load_font(TITLE_FONTNAME)

# Load the message font
MESSAGE_FONTNAME = "/fonts/cherry-11-r.bdf"
MESSAGE_FONT = bitmap_font.load_font(MESSAGE_FONTNAME)

class DiscordMessageGroup(displayio.Group, messages.DiscordMessageBase):
    """Display class for Discord messages"""

    max_lines = 5

    def __init__(self, message: str, user: str, cmd_type: int, dark_mode: bool = True) -> None:

        super().__init__()
        messages.DiscordMessageBase.__init__(self, message, user, cmd_type)

        text_color = 0xFFFFFF if dark_mode else 0x000000
        self.username_label = Label(TITLE_FONT, text=user, color=text_color, y=8)
        self.append(self.username_label)

        message_lines = layout.wrap_text(message, 26)
        self.wrapped_message = "\n".join(message_lines[:self.max_lines])

        self.message_label = Label(MESSAGE_FONT, text=self.wrapped_message, color=text_color, y=32)
        self.append(self.message_label)
