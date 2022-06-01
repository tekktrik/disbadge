# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`raspberrypi.rpi_messages`
==========================

RaspberryPi-specific Discord message class

* Author(s): Alec Delaney

"""

from typing import Dict
from shared.messages import DiscordMessageBase
from shared.uri_codec import encode_dictionary


# pylint: disable=too-few-public-methods
class RPiDiscordMessage(DiscordMessageBase):
    """The extension of DiscordMessage Base that is used by the
    Raspberry Pi"""

    def to_dict(self) -> Dict[str, str]:
        """Converts this message to a dictionary"""

        prelim_dict = {
            "message": self._message,
            "user": self._user,
            "cmdtype": str(self._cmd_type),
        }
        return encode_dictionary(prelim_dict)
