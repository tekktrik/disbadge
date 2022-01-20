"""
This is a Conference Badge type Name Tag that is intended to be displayed on
the PyBadge. Feel free to customize it to your heart's content.
"""

import time
import board
from micropython import const
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from discord_display import DiscordMessage

# Button Constants
BUTTON_LEFT = const(128)
BUTTON_UP = const(64)
BUTTON_DOWN = const(32)
BUTTON_RIGHT = const(16)
BUTTON_SEL = const(8)
BUTTON_START = const(4)
BUTTON_A = const(2)
BUTTON_B = const(1)

# Customizations
HELLO_STRING = "Hello! This is a much much longer test"
MY_NAME_STRING = "MY NAME IS"
NAME_STRING = "Blinka"
MESSAGE_FONTNAME = "/fonts/Tewi-11.bdf"
CHARACTERS_PER_LINE = 31
BACKGROUND_COLOR = 0x37393F
MESSAGE_TEXT_COLOR = 0xFFFFFF

# Make the Display Background
splash = displayio.Group()
board.DISPLAY.show(splash)

color_bitmap = displayio.Bitmap(160, 128, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)
time.sleep(3)

# Test message
notification = DiscordMessage("Tekktrik", "This is a test message!")
splash.append(notification)
time.sleep(10)
