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
#from adafruit_airlift.esp32 import ESP32
#from adafruit_ble import BLERadio
#from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
#from adafruit_ble.services.nordic import UARTService
import usb_cdc
from states import LEDStateIDs
from pybadge_messages import DiscordMessageGroup
from disbadge import DiscordPyBadge, Buttons
from shared.messages import CommandType
from states import DisplayStateIDs
from shared.uart import UARTManager

import global_state

uart = usb_cdc.data
print("uart", uart)

MESSAGE_PIN_TIME = 10
"""How long messages should be displayed before being removed"""

disbadge = DiscordPyBadge(external_speaker=True)
disbadge.set_splash(DisplayStateIDs.LOADING)


async def data_transmission():
    """Sub-sequence for handling data transmission over Serial"""

    with UARTManager(uart) as uart_manager:
        while uart_manager.data_available:
            print("AVAILABLE!")
            message_dict = uart_manager.receive()
            global_state.CURRENT_MESSAGE = DiscordMessageGroup()
            global_state.CURRENT_MESSAGE.from_dict(message_dict)
            gc.collect()
        await asyncio.sleep(0)


async def ui_management():
    """Sub-sequence for handling the user input and interface"""

    # Main loop for handling UI and buttons
    current_message = global_state.CURRENT_MESSAGE
    print(current_message)
    print(disbadge.current_message)
    if current_message != disbadge.current_message:
        
        if current_message is None:
            disbadge.set_splash(DisplayStateIDs.NO_MESSAGE)
        else:
            if current_message.cmd_type == CommandType.PING:
                led_animation_id = LEDStateIDs.PING
                new_splash_id = DisplayStateIDs.PING
            elif current_message.cmd_type == CommandType.CHEER:
                led_animation_id = LEDStateIDs.CHEER
                new_splash_id = DisplayStateIDs.CHEER
            else:
                led_animation_id = LEDStateIDs.HYPE
                new_splash_id = DisplayStateIDs.HYPE
            disbadge.set_splash(new_splash_id)
            disbadge.animation = led_animation_id
            disbadge.play_notification(new_splash_id)
            disbadge.set_splash(DisplayStateIDs.MESSAGE, message=current_message)

            popup_start_time = time.monotonic()
            while time.monotonic() < popup_start_time + (MESSAGE_PIN_TIME*60) or current_message != disbadge.current_message:
                disbadge.animate_leds()
                if disbadge.button_pressed == Buttons.BUTTON_B:
                    break
                await asyncio.sleep(0)
            disbadge.animation = LEDStateIDs.NONE
            if current_message != disbadge.current_message: # New message
                disbadge.set_splash(DisplayStateIDs.LOADING)
            else: # Timed out
                disbadge.set_splash(DisplayStateIDs.NO_MESSAGE)
                current_message = None

        print("REACHED")
        await asyncio.sleep(0)


async def main():
    """Main sequence"""

    while True:

        # Create and await tasks to achieve main functionality at this level
        data_task = asyncio.create_task(data_transmission())
        ui_task = asyncio.create_task(ui_management())
        await asyncio.gather(data_task, ui_task)

asyncio.run(main())
