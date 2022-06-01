# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`states`
========

Various program states stored in Enum-like objects

* Author(s): Alec Delaney

"""

# pylint: disable=too-few-public-methods
class DisplayStateIDs:
    """The current display state of the program"""

    LOADING = 0
    CONNECTING = 1
    NO_MESSAGE = 2
    MESSAGE = 3
    PING = 4
    CHEER = 5
    HYPE = 6
    CONNECT = 7
    WAITING = 8
    BACKGROUND = 9


# pylint: disable=too-few-public-methods
class LEDStateIDs:
    """The current LED animation state of the program"""

    NONE = 0
    PING = 1
    CHEER = 2
    HYPE = 3
