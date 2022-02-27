"""
`screens`
====================================================

Screens that are generated as part of the Discord PyBadge program

* Author(s): Alec Delaney

"""

import displayio
from adafruit_bitmap_font import bitmap_font
import adafruit_imageload
from adafruit_display_text.label import Label

try:
    from typing import Tuple
except ImportError:
    pass

# Screen properties
SCREEN_HEIGHT = 128
SCREEN_WIDTH = 160

# Load the splash font
SPLASH_FONTNAME = "/fonts/Noto-18.bdf"
SPLASH_FONT = bitmap_font.load_font(SPLASH_FONTNAME)


class SplashBackground(displayio.Group):
    """Base class that applies a solid color background as a splash screen

    :param int color: The background color of the splash screen
    """

    def __init__(self, color: int) -> None:

        super().__init__()

        self._color = color

        # TODO: This code is fine, but the background will be the same, only set once
        self._bg_bitmap = displayio.Bitmap(SCREEN_WIDTH, SCREEN_HEIGHT, 1)
        self._bg_palette = displayio.Palette(1)
        self._bg_palette[0] = self._color
        self._bg = displayio.TileGrid(
            self._bg_bitmap, pixel_shader=self._bg_palette, x=0, y=0
        )

        self.append(self._bg)


class TextSplashScreen(displayio.Group):
    """A splash screen with a text label in the center

    :param int id: The id of this splash screen
    :param str text: The text to be displayed on the screen
    :param int text_color: (Optional) The color to apply to the text, default is white
    """

    def __init__(self, screen_id: int, text: str, text_color: int = 0xFFFFFF) -> None:

        super().__init__()

        self._screen_id = screen_id
        self._text = text
        self._text_color = text_color

        self._label = Label(SPLASH_FONT, text=text, color=self._text_color)
        self._label.x = (SCREEN_WIDTH - self._label.width) // 2
        self._label.y = (SCREEN_HEIGHT - self._label.height) // 2
        self.append(self._label)


class LabeledTextSplashScreen(displayio.Group):
    """A TextSplashScreen with a label for the given text

    :param int id: The id of this splash screen
    :param str label: The text to be used as the label text
    :param str text: The text to be displayed on the screen as the message
    :param int text_color: (Optional) The color to apply to the text, default is white
    """

    def __init__(
        self, screen_id: int, label: str, message: str, text_color: int = 0xFFFFFF
    ) -> None:

        super().__init__()

        self._screen_id = screen_id
        self._text = message
        self._text_color = text_color
        self._label_label = Label(SPLASH_FONT, text=label, color=self._text_color)
        self._label_label.x = (SCREEN_WIDTH - self._label_label.width) // 2
        self._label_label.y = SCREEN_HEIGHT // 2 - self._label_label.height
        self._message_label = Label(SPLASH_FONT, text=message, color=self._text_color)
        self._message_label.x = (SCREEN_WIDTH - self._message_label.width) // 2
        self._message_label.y = SCREEN_HEIGHT // 2
        self.append(self._label_label)
        self.append(self._message_label)
