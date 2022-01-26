"""
This is a Conference Badge type Name Tag that is intended to be displayed on
the PyBadge. Feel free to customize it to your heart's content.
"""

import time
import board
from micropython import const
import displayio
import asyncio
from adafruit_airlift.esp32 import ESP32
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from pybadge_messages import DiscordMessageGroup
from display import ScreenManager, SplashBackground, TextSplashScreen
from shared.uart_manager import UARTManager

try:
    from typing import Optional
except ImportError:
    pass

# Button Constants
BUTTON_LEFT = const(7)
BUTTON_UP = const(6)
BUTTON_DOWN = const(5)
BUTTON_RIGHT = const(4)
BUTTON_SEL = const(3)
BUTTON_START = const(2)
BUTTON_A = const(1)
BUTTON_B = const(0)

screen = ScreenManager()
screen.set_loading_splash()

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

    with UARTManager(uart, ble) as uart_manager:
        while uart_manager.connected:
            while uart_manager.data_available > 0:
                message_dict = uart_manager.receive()
                CURRENT_MESSAGE.from_payload(message_dict)
            asyncio.sleep(0)

async def ui_management():

    while ble.connected:

        # Main loop for handling UI and buttons
        
        asyncio.sleep(0)

async def main():

    # Main loop
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
                await asyncio.gather(data_task, ui_task)

        # If not connected, attempt to do so
        screen.set_connecting_splash()
        for advertisement in ble.start_scan(ProvideServicesAdvertisement, timeout=1):
            advertisement: ProvideServicesAdvertisement
            if UARTService not in advertisement.services:
                continue
            ble.connect(advertisement)
            print("Connected!")

asyncio.run(main())
