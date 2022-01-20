import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

# Load the title and message font
TITLE_FONTNAME = "/fonts/cozette.bdf"
TITLE_FONT = bitmap_font.load_font(TITLE_FONTNAME)
MESSAGE_FONTNAME = "/fonts/Tewi-11.bdf"
MESSAGE_FONT = bitmap_font.load_font(MESSAGE_FONTNAME)

class DiscordMessage(displayio.Group):

    def __init__(self, username: str, message: str, dark_mode: bool = True) -> None:

        super().__init__()

        text_color = 0xFFFFFF if dark_mode else 0x000000
        self.username_label = Label(TITLE_FONT, text=username, color=text_color, y=8)
        self.append(self.username_label)

        message_lines = DiscordMessage._wrap_nicely(message, 26)
        max_lines = 4
        self.wrapped_message = "\n".join(message_lines[:max_lines])

        self.message = Label(MESSAGE_FONT, text=self.wrapped_message, color=text_color, y=32)
        self.append(self.message)

    # cribbed from adafruit_display_notification
    @staticmethod
    def _wrap_nicely(string: str, max_chars: int):
        """A helper that will return a list of lines with word-break wrapping.

        :param str string: The text to be wrapped.
        :param int max_chars: The maximum number of characters on a line before wrapping.
        """

        string = string.replace("\n", "").replace("\r", "")  # strip confusing newlines
        words = string.split(" ")
        the_lines = []
        the_line = ""
        for w in words:
            if len(the_line + " " + w) <= max_chars:
                the_line += " " + w
            else:
                the_lines.append(the_line)
                the_line = "" + w
        if the_line:  # last line remaining
            the_lines.append(the_line)
        # remove first space from first line:
        the_lines[0] = the_lines[0][1:]
        return the_lines