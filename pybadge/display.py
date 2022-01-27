import board
import displayio
from adafruit_bitmap_font import bitmap_font
import adafruit_imageload
from adafruit_display_text.label import Label
from states import StateIDs

try:
    from typing import Optional, Tuple
    from pybadge_messages import DiscordMessageGroup
except ImportError:
    pass

# Screen properties
SCREEN_HEIGHT = 128
SCREEN_WIDTH = 160

# Customizable colors
SETUP_BG_COLOR = 0x37393F
SETUP_TEXT_COLOR = 0xFFFFFF
MESSAGE_BG_COLOR = 0x37393F
MESSAGE_TEXT_COLOR = 0xFFFFFF

# Customizable default texts
LOADING_TEXT = "Loading..."
CONNECTING_TEXT = "Connecting..."
NO_MESSAGES_TEXT = "No messages!"

# Load the splash font
SPLASH_FONTNAME = "/fonts/Noto-18.bdf"
SPLASH_FONT = bitmap_font.load_font(SPLASH_FONTNAME)


class SplashBackground(displayio.Group):
    """Base class that applies a solid color background as a splash screen

    :param int id: The id of this splash screen
    :param int color: The background color of the splash screen
    """

    def __init__(self, id: int, color: int) -> None:

        super().__init__()

        self._color = color
        self._id = id

        self._bg_bitmap = displayio.Bitmap(SCREEN_WIDTH, SCREEN_HEIGHT, 1)
        self._bg_palette = displayio.Palette(1)
        self._bg_palette[0] = self._color
        self._bg = displayio.TileGrid(
            self._bg_bitmap, pixel_shader=self._bg_palette, x=0, y=0
        )

        self.append(self._bg)

    @property
    def color(self) -> str:
        """The background color of the splash screen"""
        return self._color

    @property
    def bitmap(self) -> displayio.Bitmap:
        "The bitmap associated with this splash screen background"
        return self._bg_bitmap

    @property
    def pallete(self) -> displayio.Palette:
        "The palette associated with this splash screen background"
        return self._bg_palette

    @property
    def background(self) -> displayio.TileGrid:
        """The tile grid associated with this splash screen background"""
        return self._bg

    @property
    def id(self) -> int:
        """The title of this splash screen"""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value


class TextSplashScreen(SplashBackground):
    """A splash screen with a text label in the center

    :param int id: The id of this splash screen
    :param int color: The background color of the splash screen
    :param str text: The text to be displayed on the screen
    :param int text_color: (Optional) The color to apply to the text, default is white
    """

    def __init__(
        self, id: int, color: int, text: str, text_color: int = 0xFFFFFF
    ) -> None:

        super().__init__(color, id=id)

        self._text = text
        self._text_color = text_color

        self._label = Label(SPLASH_FONT, text=text, color=self._text_color)
        self._label.x = (SCREEN_WIDTH - self._label.width) // 2
        self._label.y = (SCREEN_HEIGHT - self._label.height) // 2
        self.append(self._label)

    @property
    def text(self) -> str:
        """The text of the splash screen"""
        return self._text

    @property
    def text_color(self) -> int:
        return self._text_color


class ImageSplashScreen(SplashBackground):
    """A splash screen with an image in the center

    :param int id: The id of this splash screen
    :param int color: The background color of the splash screen
    :param str image_filename: The filename of the image to display
    :param int image_size: (Optional) The height/width of the image in pixels, default is 32
    """

    def __init__(
        self, id: int, color: int, image_filename: str, image_size: int = 32
    ) -> None:

        super().__init__(id, color)
        self._image_size = image_size

        splash_image, splash_palette = adafruit_imageload.load(image_filename)
        self._image = displayio.TileGrid(
            splash_image,
            pixel_shader=splash_palette,
            width=1,
            height=1,
            tile_height=image_size,
            tile_width=image_size,
        )
        self._image.x = (SCREEN_WIDTH - image_size) // 2
        self._image.y = (SCREEN_HEIGHT - image_size) // 2
        self.append(self._image)

    @property
    def image(self) -> displayio.TileGrid:
        """The image associated with this splash screen, as a TileGrid"""
        return self._image

    @property
    def image_size(self) -> Tuple[int, int]:
        """The image dimensions as a tuole"""
        return (self._image_size, self._image_size)


class ScreenManager:
    """A class for managing splash screens and transitions between them"""

    def __init__(self):

        # Make the Display Background
        self.splash = displayio.Group()
        board.DISPLAY.show(self.splash)

        # Display loading screen
        self.loading_splash = TextSplashScreen(
            SETUP_BG_COLOR, LOADING_TEXT, SETUP_TEXT_COLOR
        )
        self.splash.append(self.loading_splash)

        # Set up other splash screens
        self.connecting_splash = TextSplashScreen(
            StateIDs.CONNECTING, SETUP_BG_COLOR, CONNECTING_TEXT
        )
        self.no_message_splash = TextSplashScreen(
            StateIDs.NO_MESSAGE, MESSAGE_BG_COLOR, NO_MESSAGES_TEXT
        )
        self.message_splash = SplashBackground(
            StateIDs.MESSAGE, MESSAGE_BG_COLOR
        )
        self.message_splash.append(displayio.Group())
        self.ping_splash = ImageSplashScreen(
            StateIDs.PING, MESSAGE_BG_COLOR, "ping.bmp"
        )
        self.cheer_splash = ImageSplashScreen(
            StateIDs.CHEER, MESSAGE_BG_COLOR, "cheer.bmp"
        )
        self.hype_splash = ImageSplashScreen(
            StateIDs.HYPE, MESSAGE_BG_COLOR, "hype.bmp"
        )

        self.splash.insert(0, self.connecting_splash)
        self.splash.insert(0, self.no_message_splash)
        self.splash.insert(0, self.message_splash)
        self.splash.insert(0, self.ping_splash)
        self.splash.insert(0, self.cheer_splash)
        self.splash.insert(0, self.hype_splash)

    def set_splash(self, id: int, message: Optional[displayio.Group] = None) -> None:
        """Sets the splash screen

        :param int id: The id of the splash screen
        :param display.Group message: The message or Group to display
        """

        for screen in self.splash:
            screen: SplashBackground
            if screen.id == id:
                self.splash.remove(screen)
                if message:
                    screen.pop()
                    screen.append(message)
                self.splash.append(screen)
                return
        raise ValueError("Invalid screen ID")

    @property
    def current_splash(self) -> int:
        """Gets the current splash screen's title"""
        current_splash: SplashBackground = self.splash[-1]
        return current_splash.id
