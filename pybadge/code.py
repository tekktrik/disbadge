# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`code`
====================================================

Main sequence for Discord PyBadge

* Author(s): Alec Delaney

"""

import time
import board
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_wifimanager as wifimanager
import adafruit_esp32spi.adafruit_esp32spi_wsgiserver as server
from states import LEDStateIDs
from pybadge_messages import DiscordMessageGroup
from disbadge import DiscordPyBadge, Buttons
from shared.messages import CommandType
from states import DisplayStateIDs
from adafruit_wsgi.wsgi_app import WSGIApp
import global_state
from shared.secrets import secrets

try:
    import typing  # pylint: disable=unused-import
    from adafruit_wsgi.request import Request  # pylint: disable=ungrouped-imports
except ImportError:
    pass

MESSAGE_PIN_TIME = 10
"""How long messages should be displayed before being removed"""

disbadge = DiscordPyBadge(external_speaker=True)
disbadge.set_splash(DisplayStateIDs.LOADING)

# Set up ESP32
esp32_cs = DigitalInOut(board.D13)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)
esp32 = adafruit_esp32spi.ESP_SPIcontrol(
    board.SPI(), esp32_cs, esp32_ready, esp32_reset
)

disbadge.set_splash(DisplayStateIDs.CONNECTING)
wifi = wifimanager.ESPSPI_WiFiManager(esp32, secrets, attempts=3, debug=True)
wifi.connect()

web_app = WSGIApp()


@web_app.route("/message", ["POST"])
def display_message(request: Request):  # TODO: add request param
    """Function for handling data transmission over WSGI app

    :param Request request: The incoming request
    """

    print("RECEIVED NEW MESSAGE!")
    global_state.CURRENT_MESSAGE = DiscordMessageGroup()
    global_state.CURRENT_MESSAGE.from_json(request.body)
    return ("200 OK", ["Content-Type", "text/plain"], "")


@web_app.route("/activate", ["POST"])
def activate_disbadge(request: Request):  # TODO: add request param
    """Function for activating the DisBadge

    :param Request request: The incoming request
    """

    global_state.DISCORD_CONNECTION = True
    print("Activated!")
    return ("200 OK", ["Content-Type", "text/plain"], "")


@web_app.route("/sound/<setting>", ["POST"])
def set_sound(request: Request, setting: str):
    """Turn off the DisBadge sound

    :param Request request: The incoming request
    :param str setting: The sound setting
    """
    if setting == "off":
        disbadge.muted = True
    return ("200 OK", ["Content-Type", "text/plain"], "")


server.set_interface(esp32)
wsgi_server = server.WSGIServer(80, application=web_app)
wsgi_server.start()

pretty_ip_address = esp32.pretty_ip(esp32.ip_address)
disbadge.ip_address = pretty_ip_address
print(pretty_ip_address)
disbadge.set_splash(DisplayStateIDs.CONNECT)
while not global_state.DISCORD_CONNECTION:
    wsgi_server.update_poll()
disbadge.set_splash(DisplayStateIDs.NO_MESSAGE)


def main():
    """Main sequence"""

    while True:

        # Main loop for handling UI and buttons

        if not esp32.is_connected:
            disbadge.set_splash(DisplayStateIDs.CONNECTING)
            while not esp32.is_connected:
                wifi.reset()
                pass

        wsgi_server.update_poll()

        # Guard statement for message equality
        if global_state.CURRENT_MESSAGE == disbadge.current_message:
            continue

        # Check if no messsage
        if global_state.CURRENT_MESSAGE is None:
            disbadge.set_splash(DisplayStateIDs.NO_MESSAGE)
            continue

        # Handle actual message
        disbadge.flush_inputs()
        if global_state.CURRENT_MESSAGE.cmd_type == CommandType.PING:
            led_animation_id = LEDStateIDs.PING
            new_splash_id = DisplayStateIDs.PING
        elif global_state.CURRENT_MESSAGE.cmd_type == CommandType.CHEER:
            led_animation_id = LEDStateIDs.CHEER
            new_splash_id = DisplayStateIDs.CHEER
        else:
            led_animation_id = LEDStateIDs.HYPE
            new_splash_id = DisplayStateIDs.HYPE
        disbadge.set_splash(new_splash_id)
        disbadge.animation = led_animation_id
        disbadge.play_notification(new_splash_id)
        disbadge.set_splash(
            DisplayStateIDs.MESSAGE, message=global_state.CURRENT_MESSAGE
        )

        # Start LED animation clock
        popup_start_time = time.monotonic()
        while (
            time.monotonic() < popup_start_time + (MESSAGE_PIN_TIME * 60)
            and global_state.CURRENT_MESSAGE == disbadge.current_message
        ):
            disbadge.animate_leds()
            wsgi_server.update_poll()
            disbadge.update_inputs()
            if disbadge.button_pressed == Buttons.BUTTON_B:
                break
        disbadge.animation = LEDStateIDs.NONE
        disbadge.animate_leds()
        disbadge.play_notification(None)

        # Check if new message available
        if global_state.CURRENT_MESSAGE == disbadge.current_message:  # New message
            disbadge.set_splash(DisplayStateIDs.NO_MESSAGE)
            global_state.CURRENT_MESSAGE = None


main()
