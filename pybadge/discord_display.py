import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import shared.layout_helper as layout
import shared.content as content

# Load the title font
TITLE_FONTNAME = "/fonts/cozette.bdf"
TITLE_FONT = bitmap_font.load_font(TITLE_FONTNAME)

# Load the message font
MESSAGE_FONTNAME = "/fonts/Tewi-11.bdf"
MESSAGE_FONT = bitmap_font.load_font(MESSAGE_FONTNAME)

class DiscordMessageGroup(content.DiscordMessageBase, displayio.Group):
    """Display class for Discord messages"""

    def __init__(self, message: str, username: str, cmd_type: int, dark_mode: bool = True) -> None:

        super().__init__(message, username)

        text_color = 0xFFFFFF if dark_mode else 0x000000
        self.username_label = Label(TITLE_FONT, text=username, color=text_color, y=8)
        self.append(self.username_label)

        message_lines = layout.wrap_text(message, 26)
        max_lines = 4
        self.wrapped_message = "\n".join(message_lines[:max_lines])

        self.message_label = Label(MESSAGE_FONT, text=self.wrapped_message, color=text_color, y=32)
        self.append(self.message_label)
