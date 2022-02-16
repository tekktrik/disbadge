import board
import displayio
from adafruit_bitmap_font import bitmap_font
import adafruit_imageload
from adafruit_display_text.label import Label
from states import DisplayStateIDs

try:
    from typing import Optional, Tuple
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

    :param int id: The id of this splash screen
    :param int color: The background color of the splash screen
    """

    def __init__(self, screen_id: int, color: int) -> None:

        super().__init__()

        self._color = color
        self._screen_id = screen_id

        bg_bitmap = displayio.Bitmap(SCREEN_WIDTH, SCREEN_HEIGHT, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = self._color
        self._bg = displayio.TileGrid(
            bg_bitmap, pixel_shader=bg_palette, x=0, y=0
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
    def screen_id(self) -> int:
        """The title of this splash screen"""
        return self._screen_id

    @screen_id.setter
    def screen_id(self, value: int) -> None:
        self._screen_id = value


class TextSplashScreen(SplashBackground):
    """A splash screen with a text label in the center

    :param int id: The id of this splash screen
    :param int color: The background color of the splash screen
    :param str text: The text to be displayed on the screen
    :param int text_color: (Optional) The color to apply to the text, default is white
    """

    def __init__(
        self, screen_id: int, color: int, text: str, text_color: int = 0xFFFFFF
    ) -> None:

        super().__init__(screen_id, color)

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
        self, screen_id: int, color: int, image_filename: str, image_size: int = 32
    ) -> None:

        super().__init__(screen_id, color)
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
