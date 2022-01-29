"""
`disbadge`
====================================================

Manager for the PyBadge that handles user input, displays, and sounds

* Author(s): Alec Delaney

"""

import gc
import board
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
from screens import SplashBackground, TextSplashScreen, ImageSplashScreen

try:
    from typing import Optional, Union
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

    :param bool external_speaker: Whether the PyBadge is set up to use an
        external speaker; default is False
    """

    def __init__(self, external_speaker: bool = False) -> None:

        # Make the Display Background
        self.splash = displayio.Group()
        board.DISPLAY.show(self.splash)

        # Display loading screen details
        self._current_message = None
        self._splashes = {
            DisplayStateIDs.LOADING: {
                "type": "ts",
                "bg": SETUP_BG_COLOR,
                "text": LOADING_TEXT,
            },
            DisplayStateIDs.CONNECTING: {
                "type": "ts",
                "bg": SETUP_BG_COLOR,
                "text": CONNECTING_TEXT,
            },
            DisplayStateIDs.NO_MESSAGE: {
                "type": "ts",
                "bg": MESSAGE_BG_COLOR,
                "text": NO_MESSAGES_TEXT,
            },
            DisplayStateIDs.MESSAGE: {
                "type": "s",
                "bg": MESSAGE_BG_COLOR,
            },
            DisplayStateIDs.PING: {
                "type": "is",
                "bg": MESSAGE_BG_COLOR,
                "image": "ping.bmp",
            },
            DisplayStateIDs.CHEER: {
                "type": "is",
                "bg": MESSAGE_BG_COLOR,
                "image": "cheer.bmp",
            },
            DisplayStateIDs.HYPE: {
                "type": "is",
                "bg": MESSAGE_BG_COLOR,
                "image": "hype.bmp",
            },
        }

        # Initialize LED animations
        self._neopixels = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.25)
        self._blank_animation = Solid(self._neopixels, color=BLACK)
        self._current_animation = self._blank_animation
        self._animations = {
            LEDStateIDs.PING: Pulse(self._neopixels, speed=0.5, color=RED, period=2),
            LEDStateIDs.CHEER: Rainbow(self._neopixels, speed=0.1, period=0.75),
            LEDStateIDs.HYPE: RainbowSparkle(self._neopixels, speed=0.1, period=0.75),
            LEDStateIDs.NONE: self._blank_animation,
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
            DisplayStateIDs.PING: {"type": "mp3", "file": "sound/Victory Stinger.mp3"},
            DisplayStateIDs.CHEER: {"type": "wav", "file": "sound/chipquest.wav"},
            DisplayStateIDs.HYPE: {"type": "wav", "file": "sound/Victory.wav"},
        }
        if external_speaker:
            self.speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
            self.speaker_enable.switch_to_output()

        self.audio = AudioOut(board.SPEAKER)
        """The audio object for the DiscordPyBadge"""

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
    def animation(self, animation_id: int) -> None:
        self._current_animation = self._animations.get(animation_id)
        gc.collect()

    def animate_leds(self) -> None:
        """Animates the NeoPixels if there is a current animation"""
        self._current_animation.animate()

    def _generate_screen(
        self, screen_id: int, message: Optional[displayio.Group] = None
    ) -> SplashBackground:
        splash_reqs = self._splashes[screen_id]
        if splash_reqs["type"] == "ts":
            new_splash = TextSplashScreen(
                screen_id, splash_reqs["bg"], splash_reqs["text"]
            )
        elif splash_reqs["type"] == "s":
            new_splash = SplashBackground(screen_id, splash_reqs["bg"])
            new_message = message if message else displayio.Group()
            self._current_message = message if message else None
            new_splash.append(new_message)
        elif splash_reqs["type"] == "is":
            new_splash = ImageSplashScreen(
                screen_id, splash_reqs["color"], splash_reqs["image"]
            )
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
        if len(self.splash) > 1:
            self.splash.remove(self.splash[0])
            gc.collect()

    @property
    def current_splash(self) -> int:
        """Gets the current splash screen's title"""
        current_splash: SplashBackground = self.splash[-1]
        return current_splash.screen_id

    def _generate_audio_file(self, sound_id: int) -> Union[MP3Decoder, WaveFile]:
        sound_reqs = self._sounds.get(sound_id)
        if not sound_reqs:
            raise ValueError("Invalid sound id")
        if sound_reqs["type"] == "mp3":
            return MP3Decoder(open(sound_reqs["file"], "rb"))
        return WaveFile(open(sound_reqs["file"], "rb"))

    def play_notification(self, sound_id: int) -> None:
        """Plays a notification sound, and pauses execution while doing so

        :param int sound_id: The id of the notification sound
        """

        self._current_sound = self._generate_audio_file(sound_id)
        if self._current_sound:
            self.speaker_enable.value = True
            self.audio.play(self._current_sound)
            while self.audio.playing:
                pass
            self.speaker_enable.value = False
            self._current_sound.deinit()
            gc.collect()
