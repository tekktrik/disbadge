import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import shared.layout_helper as layout
import shared.content as content

# Load the title font
TITLE_FONTNAME = "/fonts/cherry-13-b.bdf"
TITLE_FONT = bitmap_font.load_font(TITLE_FONTNAME)

# Load the message font
MESSAGE_FONTNAME = "/fonts/cherry-11-r.bdf"
MESSAGE_FONT = bitmap_font.load_font(MESSAGE_FONTNAME)

class DiscordMessageGroup(displayio.Group, content.DiscordMessageBase):
    """Display class for Discord messages"""

    def __init__(self, message: str, username: str, cmd_type: int, dark_mode: bool = True) -> None:
    max_lines = 5

        content.DiscordMessageBase.__init__(message, username, cmd_type)
        displayio.Group.__init__()

        text_color = 0xFFFFFF if dark_mode else 0x000000
        self.username_label = Label(TITLE_FONT, text=username, color=text_color, y=8)
        self.append(self.username_label)

        message_lines = layout.wrap_text(message, 26)
        self.wrapped_message = "\n".join(message_lines[:self.max_lines])

        self.message_label = Label(MESSAGE_FONT, text=self.wrapped_message, color=text_color, y=32)
        self.append(self.message_label)
