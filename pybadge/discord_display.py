import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

# Load the message font
MESSAGE_FONTNAME = "/fonts/cozette.bdf"
MESSAGE_FONT = bitmap_font.load_font(MESSAGE_FONTNAME)

class DiscordMessage(displayio.Group):

    def __init__(self, username: str, message: str, dark_mode: bool = True) -> None:

        super().__init__()

        text_color = 0xFFFFFF if dark_mode else 0x000000
        self.username_label = Label(MESSAGE_FONT, text=username, color=text_color, y=8)
        self.append(self.username_label)

        message_lines = DiscordMessage._wrap_nicely(message, 26)
        max_lines = 4
        self.wrapped_message = "\n".join(message_lines[:max_lines])

        self.message = Label(MESSAGE_FONT, text=self.wrapped_message, color=text_color, y=32)
        self.append(self.message)

    # cribbed from adafruit_display_notification
