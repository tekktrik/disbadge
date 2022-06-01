# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`disbadge`
==========

Manager for the PyBadge that handles user input, displays, and sounds

* Author(s): Alec Delaney

"""

import gc
import board
import time
from micropython import const
from keypad import ShiftRegisterKeys, Event
import neopixel
import digitalio
import displayio
from audioio import AudioOut
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import RED, BLACK
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from audiocore import WaveFile
from audiomp3 import MP3Decoder
from states import DisplayStateIDs, LEDStateIDs
from screens import SplashBackground, TextSplashScreen, LabeledTextSplashScreen

try:
    from typing import Optional, Union
    from pybadge_messages import DiscordMessageGroup
    from adafruit_led_animation.animation import Animation
except ImportError:
    pass

# Customizable colors
SETUP_BG_COLOR = 0x37393F
SETUP_TEXT_COLOR = 0xFFFFFF
MESSAGE_BG_COLOR = 0x37393F
MESSAGE_TEXT_COLOR = 0xFFFFFF

# Customizable default texts
LOADING_TEXT = "Loading..."
CONNECTING_TEXT = "Connecting..."
NO_MESSAGES_TEXT = "No messages!"


# pylint: disable=too-few-public-methods
class Buttons:
    """An enum-like class for the button constants"""

    NONE = const(8)
    BUTTON_LEFT = const(7)
    BUTTON_UP = const(6)
    BUTTON_DOWN = const(5)
    BUTTON_RIGHT = const(4)
    BUTTON_SEL = const(3)
    BUTTON_START = const(2)
    BUTTON_A = const(1)
    BUTTON_B = const(0)


# pylint: disable=too-many-instance-attributes, no-member
class DiscordPyBadge:
    """A helper class that manages the IO for the PyBadge, including NeoPixels,
    sound, and button inputs

    :param str ip_address: The IP address of the Disbadge
    :param bool external_speaker: Whether the PyBadge is set up to use an
        external speaker; default is False
    """

    def __init__(
        self, ip_address: Optional[str] = None, external_speaker: bool = False
    ) -> None:

        # Set IP address
        self._ip_address = ip_address

        # Display loading screen details
        self._current_message = None
        self._splashes = {
            DisplayStateIDs.LOADING: {
                "type": "ts",
                "text": LOADING_TEXT,
            },
            DisplayStateIDs.CONNECTING: {
                "type": "ts",
                "text": CONNECTING_TEXT,
            },
            DisplayStateIDs.NO_MESSAGE: {
                "type": "ts",
                "text": NO_MESSAGES_TEXT,
            },
            DisplayStateIDs.MESSAGE: {
                "type": "b",
            },
            DisplayStateIDs.PING: {
                "type": "ts",
                "text": "!!!",
            },
            DisplayStateIDs.CHEER: {
                "type": "ts",
                "text": ":D",
            },
            DisplayStateIDs.HYPE: {
                "type": "ts",
                "text": "Hype!",
            },
            DisplayStateIDs.CONNECT: {
                "type": "lts",
                "text": "IP:",
            },
            DisplayStateIDs.WAITING: {
                "type": "ts",
                "text": "Activating...",
            },
            DisplayStateIDs.BACKGROUND: {
                "type": "s",
                "bg": MESSAGE_BG_COLOR,
            },
        }

        # Initialize LED animations
        self._neopixels = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.25)
        self._animations = {
            LEDStateIDs.PING: {
                "type": "pulse",
                "speed": 0.5,
                "color": RED,
                "period": 2,
            },
            LEDStateIDs.CHEER: {"type": "rainbow", "speed": 0.1, "period": 0.75},
            LEDStateIDs.HYPE: {"type": "rainbowsparkle", "speed": 0.1, "period": 0.75},
            LEDStateIDs.NONE: {"type": "solid", "color": BLACK},
        }

        # Initialize keypad-related functionalities
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

        # Initialize sounds
        self._current_sound = None
        self._sounds = {
            DisplayStateIDs.PING: {"type": "wav", "file": "sounds/vgdeathsound.wav"},
            DisplayStateIDs.CHEER: {"type": "wav", "file": "sounds/chipquest.wav"},
            DisplayStateIDs.HYPE: {"type": "wav", "file": "sounds/Victory.wav"},
        }
        if external_speaker:
            self.external_speaker = True
            self.speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
            self.speaker_enable.switch_to_output()
        else:
            self.external_speaker = False

        self.muted = False

        self.audio = AudioOut(board.SPEAKER)
        """The audio object for the DiscordPyBadge"""

        # Make the Display Background
        self.splash = self._generate_screen(DisplayStateIDs.BACKGROUND)
        board.DISPLAY.show(self.splash)

    @property
    def ip_address(self) -> Optional[str]:
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address: str) -> None:
        self._ip_address = ip_address

    def update_inputs(self) -> bool:
        """Get the latest button press Event"""

        new_event = self._pad.events.get_into(self._event)
        if self._event is None or self._event.released or not new_event:
            self._event = Event(8)
            return False
        return True

    @property
    def button_pressed(self) -> int:
        """The key number of the button pressed"""
        return self._event.key_number

    def flush_inputs(self):
        """Flushes the input of button presses"""
        while self.button_pressed != Buttons.NONE:
            self.update_inputs()

    @property
    def animation(self) -> int:
        """The ID of the current animation"""
        return self._current_animation

    @animation.setter
    def animation(self, animation_id: int) -> None:
        self._current_animation = self._generate_led_animation(animation_id)
        gc.collect()

    def animate_leds(self) -> None:
        """Animates the NeoPixels if there is a current animation"""
        self._current_animation.animate()

    def _generate_led_animation(self, animation_id: int) -> Animation:
        """Dynamically generates the LED animation object

        :param int animation_id: The animation ID
        """

        animation_reqs = self._animations[animation_id]
        if animation_reqs["type"] == "pulse":
            animation_class = Pulse
        elif animation_reqs["type"] == "rainbow":
            animation_class = Rainbow
        elif animation_reqs["type"] == "rainbowsparkle":
            animation_class = RainbowSparkle
        elif animation_reqs["type"] == "solid":
            animation_class = Solid
        true_reqs = animation_reqs.copy()
        del true_reqs["type"]
        true_reqs["pixel_object"] = self._neopixels
        return animation_class(**true_reqs)

    def _generate_screen(
        self, screen_id: int, message: Optional[displayio.Group] = None
    ) -> SplashBackground:
        """Dynamically generates the screen to show

        :param int screen_id: The screen ID
        :param displayio.Group message: (Optional) The message
        """

        self._current_message = message if message else None
        splash_reqs = self._splashes[screen_id]
        if splash_reqs["type"] == "ts":
            new_splash = TextSplashScreen(screen_id, splash_reqs["text"])
        elif splash_reqs["type"] == "b":
            new_splash = message if message else displayio.Group()
        elif splash_reqs["type"] == "lts":
            new_splash = LabeledTextSplashScreen(
                screen_id, splash_reqs["text"], self.ip_address
            )
        elif splash_reqs["type"] == "s":
            new_splash = SplashBackground(splash_reqs["bg"])
        return new_splash

    def set_splash(
        self, screen_id: int, message: Optional[displayio.Group] = None
    ) -> None:
        """Sets the splash screen

        :param int screen_id: The id of the splash screen
        :param display.Group message: The message or Group to display
        """

        new_splash = self._generate_screen(screen_id, message)
        self.splash.append(new_splash)
        while len(self.splash) > 2:
            self.splash.remove(self.splash[1])
        gc.collect()

    @property
    def current_message(self) -> Optional[DiscordMessageGroup]:
        """The current message being displayed"""
        return self._current_message

    @property
    def current_splash(self) -> int:
        """Gets the current splash screen's title"""
        current_splash: SplashBackground = self.splash[-1]
        return current_splash.screen_id

    def _generate_audio_file(self, sound_id: int) -> Union[MP3Decoder, WaveFile]:
        """Dynamically generate the sound object

        :param int sound_id: The sound ID
        """

        sound_reqs = self._sounds.get(sound_id)
        if not sound_reqs:
            raise ValueError("Invalid sound id")
        if sound_reqs["type"] == "mp3":
            return MP3Decoder(open(sound_reqs["file"], "rb"))
        return WaveFile(open(sound_reqs["file"], "rb"))

    def play_notification(self, sound_id: Optional[int]) -> None:
        """Plays a notification sound, and pauses execution while doing so
        (still animates LEDs, however)

        :param int sound_id: (Optional) The id of the notification sound,
            stops playing if ``None``
        """

        if sound_id is None:
            self._current_sound = None
            gc.collect()
            return

        if self.muted:
            start_time = time.monotonic()
            end_time = start_time + 4
            while time.monotonic() < end_time:
                if self._current_animation:
                    self._current_animation.animate()
        else:
            self._current_sound = self._generate_audio_file(sound_id)
            if self._current_sound:
                if self.external_speaker:
                    self.speaker_enable.value = True
                self.audio.play(self._current_sound)
                while self.audio.playing:
                    if self._current_animation:
                        self._current_animation.animate()
                if self.external_speaker:
                    self.speaker_enable.value = False
                self._current_sound.deinit()
                gc.collect()
