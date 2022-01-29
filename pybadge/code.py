"""
`code`
====================================================

Main sequence for Discord PyBadge

* Author(s): Alec Delaney

"""

import asyncio
import gc
import time
import board
from adafruit_airlift.esp32 import ESP32
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from pybadge.states import LEDStateIDs
from pybadge_messages import DiscordMessageGroup
from disbadge import DiscordPyBadge, Buttons
from shared.messages import CommandType
from states import DisplayStateIDs
from shared.uart import UARTManager

MESSAGE_PIN_TIME = 10
"""How long messages should be displayed before being removed"""

disbadge = DiscordPyBadge(external_speaker=True)
disbadge.set_splash(DisplayStateIDs.LOADING)

# Set up Bluetooth
esp32 = ESP32(
    reset=board.D12,
    gpio0=board.D10,
    busy=board.D11,
    chip_select=board.D13,
    tx=board.TX,
    rx=board.RX,
)
adapter = esp32.start_bluetooth()
ble = BLERadio(adapter)

CURRENT_MESSAGE = DiscordMessageGroup()


async def data_transmission(uart: UARTService):
    """Sub-sequence for handling data transmission over BLE UART

    :param UARTService uart: The UARTService connection object
    """

    with UARTManager(uart, ble) as uart_manager:
        while uart_manager.connected:
            while uart_manager.data_available:
                message_dict = uart_manager.receive()
                CURRENT_MESSAGE = DiscordMessageGroup()
                CURRENT_MESSAGE.from_dict(message_dict)
                # gc.collect()
            asyncio.sleep(0)


async def ui_management():
    """Sub-sequence for handling the user input and interface"""

    while ble.connected:

        # Main loop for handling UI and buttons
        if CURRENT_MESSAGE != disbadge.current_message:
            
            if CURRENT_MESSAGE is None:
                disbadge.set_splash(DisplayStateIDs.NO_MESSAGE)
            else:
                CURRENT_MESSAGE: DiscordMessageGroup
                if CURRENT_MESSAGE.cmd_type == CommandType.PING:
                    led_animation_id = LEDStateIDs.PING
                    new_splash_id = DisplayStateIDs.PING
                elif CURRENT_MESSAGE.cmd_type == CommandType.CHEER:
                    led_animation_id = LEDStateIDs.CHEER
                    new_splash_id = DisplayStateIDs.CHEER
                else:
                    led_animation_id = LEDStateIDs.HYPE
                    new_splash_id = DisplayStateIDs.HYPE
                disbadge.set_splash(new_splash_id)
                disbadge.animation = led_animation_id
                disbadge.play_notification(new_splash_id)
                disbadge.set_splash(DisplayStateIDs.MESSAGE, message=CURRENT_MESSAGE)

                popup_start_time = time.monotonic()
                while time.monotonic() < popup_start_time + (MESSAGE_PIN_TIME*60) or CURRENT_MESSAGE != disbadge.current_message:
                    disbadge.animate_leds()
                    if disbadge.button_pressed == Buttons.BUTTON_B:
                        break
                    asyncio.sleep(0)
                disbadge.animation = LEDStateIDs.NONE
                if CURRENT_MESSAGE != disbadge.current_message: # New message
                    disbadge.set_splash(DisplayStateIDs.LOADING)
                    continue
                else: # Timed out
                    disbadge.set_splash(DisplayStateIDs.NO_MESSAGE)
                    CURRENT_MESSAGE = None

        asyncio.sleep(0)


def main():
    """Main sequence"""

    while True:

        # If connected, look through connections and connect to one with UARTService
        if ble.connected and any(
            UARTService in connection for connection in ble.connections
        ):
            print("UARTService found in connection, getting connection...")
            for connection in ble.connections:
                if UARTService not in connection:
                    continue
                uart: UARTService = connection[UARTService]
                print("UARTService connected!")

                # Create and await tasks to achieve main functionality at this level
                data_task = asyncio.create_task(data_transmission(uart))
                ui_task = asyncio.create_task(ui_management())
                asyncio.gather(data_task, ui_task)

        # If not connected, attempt to do so
        disbadge.set_splash(DisplayStateIDs.CONNECTING)
        for advertisement in ble.start_scan(ProvideServicesAdvertisement, timeout=1):
            advertisement: ProvideServicesAdvertisement
            if UARTService not in advertisement.services:
                continue
            ble.connect(advertisement)
            print("Connected!")


main()
