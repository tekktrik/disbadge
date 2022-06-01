# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`pybadge_messages`
====================================================

PyBadge-specific Discord message class that also inherits from
displayio.Group

* Author(s): Alec Delaney

"""

import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from shared import layout, messages
from shared.uri_codec import decode_payload


try:
    import typing  # pylint: disable=unused-import
    from io import StringIO
except ImportError:
    pass

# Load the title font
TITLE_FONTNAME = "/fonts/cherry-13-b.bdf"
TITLE_FONT = bitmap_font.load_font(TITLE_FONTNAME)

# Load the message font
MESSAGE_FONTNAME = "/fonts/cherry-11-r.bdf"
MESSAGE_FONT = bitmap_font.load_font(MESSAGE_FONTNAME)


# pylint: disable=too-many-instance-attributes,abstract-method
class DiscordMessageGroup(displayio.Group, messages.DiscordMessageBase):
    """Display class for Discord messages, as both a displayio Group and
    an extension of DiscordMessageBase

    :param str message: (Optional) The Discord message, default is a
        blank string
    :param str user: (Optional) The message sender, default is a
        blank string
    :param int cmd_type: (Optional) The command type used to send the
        message, default is message.CommandType.NONE
    :param bool dark_mode: (Optional) Whether dark mode should be used
        for text color, default is True
    """

    max_lines = 5
    """The max number of lines the message can be"""

    def __init__(
        self,
        message: str = "",
        user: str = "",
        cmd_type: int = messages.CommandType.NONE,
        dark_mode: bool = True,
    ) -> None:

        super().__init__()

        self._text_color = 0xFFFFFF if dark_mode else 0x000000
        self._message_label = None
        self._username_label = None
        self._cmd_type = cmd_type

        self._user = user
        self._message = message
        self.user = self._user
        self.message = self._message

    @property
    def user(self) -> str:
        """The user that sent the message"""
        return self._user

    @user.setter
    def user(self, name: str) -> None:

        self._user = name

        if self._username_label:
            self.remove(self._username_label)

        self._username_label = Label(
            TITLE_FONT, text=self.username, color=self._text_color, y=8
        )
        self.append(self._username_label)
        self._message_label = None

    @property
    def message(self) -> str:
        """The Discord message that was sent"""
        return self._message

    @message.setter
    def message(self, text: str) -> None:

        self._message = text

        if self._message_label:
            self.remove(self._message_label)

        message_lines = layout.wrap_text(text, 26)
        self._wrapped_message = "\n".join(message_lines[: self.max_lines])

        self._message_label = Label(
            MESSAGE_FONT, text=self._wrapped_message, color=self._text_color, y=32
        )
        self.append(self._message_label)

    def from_json(self, payload: StringIO) -> None:
        """Turns a dict into a DiscordMessageGroup.  The dict must have keys
        for 'message', 'user', and 'cmd_type'

        :param StringIO payload: The payload string
        """

        payload = payload.read()
        dict_object = decode_payload(payload)
        self.message = dict_object["message"]
        self.user = dict_object["user"]
        self._cmd_type = int(dict_object["cmdtype"])
