import board
from micropython import const
from keypad import ShiftRegisterKeys, Event
import neopixel
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import RED, BLACK
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from states import StateIDs

try:
    from typing import Optional
    from adafruit_led_animation.animation import Animation
except ImportError:
    pass

class Buttons:
    """An enum-like class for the button constants"""
    BUTTON_LEFT = const(7)
    BUTTON_UP = const(6)
    BUTTON_DOWN = const(5)
    BUTTON_RIGHT = const(4)
    BUTTON_SEL = const(3)
    BUTTON_START = const(2)
    BUTTON_A = const(1)
    BUTTON_B = const(0)


class IOManager:
    """A helper class that manages the IO for the PyBadge, including NeoPixels,
    sound, and button inputs
    """

    def __init__(self):

        self._pad = ShiftRegisterKeys(
            clock=board.BUTTON_CLOCK,
            data=board.BUTTON_OUT,
            latch=board.BUTTON_LATCH,
            key_count=8,
            value_when_pressed=True,
            interval=0.1,
            max_events=1,
        )

        self._event = Event(8)

        self._neopixels = neopixel.NeoPixel(board.NEOPIXEL,
            5,
            pixel_order=neopixel.GRB,
            brightness=0.2,
            auto_write=False)

        self._current_animation = None
        self._blank_animation = Solid(self._neopixels, color=BLACK)
        self._animations = {
            StateIDs.PING: Pulse(self._neopixels, speed=0.5, color=RED, period=2),
            StateIDs.CHEER: Rainbow(self._neopixels, speed=0.1, period=0.75),
            StateIDs.HYPE: RainbowSparkle(self._neopixels, speed=0.1, period=0.75),
            StateIDs.MESSAGE: self._blank_animation,
            StateIDs.NO_MESSAGE: self._blank_animation,
        }

    def update_inputs(self) -> bool:
        """Get the latest button press Event
        
        :return: Whether the lastest event was a press
        :rtype: bool
        """

        self._pad.events.get_into(self._event)
        if self._event.released:
            self._event = Event(8)
            return False
        return True

    @property
    def button_pressed(self) -> int:
        """The key number of the button pressed"""
        return self._event.key_number

    @property
    def animation(self) -> int:
        """The ID of the current animation"""
        return self._current_animation

    @animation.setter
    def animation(self, id: int) -> None:
        self._current_animation = self._animations.get(id)

    def animate_leds(self) -> None:
        """Animates the NeoPixels if there is a current animation"""
        self._current_animation.animate()
