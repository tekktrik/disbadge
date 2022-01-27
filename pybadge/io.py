import board
from micropython import const
from keypad import ShiftRegisterKeys, Event
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import RED
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from states import StateIDs

try:
    from typing import Optional
except ImportError:
    pass


class IOManager:
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
        self._animations = {
            StateIDs.PING: Pulse(self._neopixels, speed=0.5, color=RED, period=2),
            StateIDs.CHEER: Rainbow(self._neopixels, speed=0.1, period=0.75),
            StateIDs.HYPE: RainbowSparkle(self._neopixels, speed=0.1, period=0.75),
            StateIDs.MESSAGE: None,
            StateIDs.NO_MESSAGE: None,
        }

    def update_inputs(self) -> bool:
        self._pad.events.get_into(self._event)
        if self._event.released:
            self._event = Event(8)
            return False
        return True

    @property
    def button_pressed(self) -> int:
        return self._event.key_number

    @property
    def animation(self) -> Optional[int]:
        return self._current_animation

    @animation.setter
    def animation(self, id: int) -> None:
        self._current_animation = self._animations.get(id)