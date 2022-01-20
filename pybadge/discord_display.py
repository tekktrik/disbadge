import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

# Load the message font
MESSAGE_FONTNAME = "/fonts/cozette.bdf"
MESSAGE_FONT = bitmap_font.load_font(MESSAGE_FONTNAME)

class DiscordMessage(displayio.Group):

    def __init__(self, username: str, message: str) -> None:
        username_label = Label(MESSAGE_FONT, text=username)