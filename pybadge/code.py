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

# Load the Hello font
large_font = bitmap_font.load_font(MESSAGE_FONTNAME)
large_font.load_glyphs(HELLO_STRING.encode('utf-8'))

# Setup and Center the Hello Label
hello_label = Label(large_font, text=HELLO_STRING)
(x, y, w, h) = hello_label.bounding_box
print(x)
print(y)
print(w)
print(h)
hello_label.x = (80 - w // 2)
hello_label.y = 15
hello_label.color = MESSAGE_TEXT_COLOR
splash.append(hello_label)
time.sleep(10)
splash.remove(hello_label)
splash.append(hello_label)
