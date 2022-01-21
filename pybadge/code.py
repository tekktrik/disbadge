"""
This is a Conference Badge type Name Tag that is intended to be displayed on
the PyBadge. Feel free to customize it to your heart's content.
"""

import time
import board
from micropython import const
import displayio
from adafruit_airlift.esp32 import ESP32
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from discord_display import DiscordMessageGroup
from screen_displays import ScreenManager, SplashBackground, TextSplashScreen

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

# Test message
notification = DiscordMessageGroup("This is a test message! It is considerably longer than the previous message, but this will let me test the wrapping and cutoff of texts.", "Tekktrik", 0)
splash.append(notification)
time.sleep(10)
