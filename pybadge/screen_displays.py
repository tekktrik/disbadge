import board
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label

try:
    from discord_display import DiscordMessageGroup
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

    def __init__(self, color: int) -> None:

        super().__init__()

        self._color = color

        self._bg_bitmap = displayio.Bitmap(SCREEN_WIDTH, SCREEN_HEIGHT, 1)
        self._bg_palette = displayio.Palette(1)
        self._bg_palette[0] = self._color
        self._bg = displayio.TileGrid(self._bg_bitmap,
                                        pixel_shader=self._bg_palette,
                                        x=0, y=0)

        self.append(self._bg)

    @property
    def color(self) -> str:
        return self._color

    @property
    def bitmap(self) -> displayio.Bitmap:
        return self._bg_bitmap

    @property
    def pallete(self) -> displayio.Palette:
        return self._bg_palette

    @property
    def background(self) -> displayio.TileGrid:
        return self._bg

class TextSplashScreen(SplashBackground):

    def __init__(self, color: int, text: str, text_color: int = 0xFFFFFF) -> None:

        super().__init__(color)

        self._text = text
        self._text_color = text_color

        self._set_label(text)

    def _set_label(self, text: str) -> None:
        self._label = Label(SPLASH_FONT, text=text, color=self._text_color)
        self._label.x = (SCREEN_WIDTH - self._label.width) // 2
        self._label.y = (SCREEN_HEIGHT - self._label.height) // 2
        self.append(self._label)

    @property
    def text(self) -> str:
        return self._text

    @property
    def text_color(self) -> int:
        return self._text_color

class ScreenManager:

    def __init__(self):

        # Make the Display Background
        self.splash = displayio.Group()
        board.DISPLAY.show(self.splash)

        # Display loading screen
        self.loading_splash = TextSplashScreen(SETUP_BG_COLOR, LOADING_TEXT, SETUP_TEXT_COLOR)
        self.splash.append(self.loading_splash)

        # Set up other splash screens
        self.connecting_splash = TextSplashScreen(SETUP_BG_COLOR, CONNECTING_TEXT)
        self.no_message_splash = TextSplashScreen(MESSAGE_BG_COLOR, NO_MESSAGES_TEXT)
        self.has_message_splash = SplashBackground(MESSAGE_BG_COLOR)
        self.has_message_splash.append(displayio.Group())
        # TODO: Add notification popup screen
        print(len(self.splash))
        self.splash.insert(0, self.connecting_splash)
        self.splash.insert(0, self.no_message_splash)
        self.splash.insert(0, self.has_message_splash)

    def set_loading_splash(self) -> None:

        self.splash.remove(self.loading_splash)
        self.splash.append(self.loading_splash)

    def set_connecting_splash(self) -> None:

        self.splash.remove(self.connecting_splash)
        self.splash.append(self.connecting_splash)

    def set_no_message_splash(self) -> None:

        self.splash.remove(self.no_message_splash)
        self.splash.append(self.no_message_splash)

    def set_message_splash(self, message: displayio.Group) -> None:

        self.splash.remove(self.has_message_splash)
        self.has_message_splash.pop()
        self.has_message_splash.append(message)
        self.splash.append(self.has_message_splash)
