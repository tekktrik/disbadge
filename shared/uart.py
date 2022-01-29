"""
`shared.messages`
====================================================

Class for managing UART for both the PyBadge and Raspberry Pi

* Author(s): Alec Delaney

"""

import json

try:
    from typing import Dict, Any, Optional, Type
    from types import TracebackType
    from adafruit_ble.services.nordic import UARTService
    from adafruit_ble import BLERadio
except ImportError:
    pass


class UARTManager:
    """Effectively a wrapper class for UARTService that adds functionality
    for managing UART for our purposes

    :param UARTService uart_connection: The UART service connection
    :param BLERadio ble_radio: The BLE radio object
    """

    def __init__(self, uart_connection: UARTService, ble_radio: BLERadio) -> None:
        self._uart = uart_connection
        self._ble = ble_radio
        self._buffer = bytearray(100)

    def __enter__(self) -> "UARTManager":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[type]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self._uart.reset_input_buffer()

    def _prepare_buffer(self, payload_length: int) -> None:
        if len(self._buffer) > payload_length:
            self._buffer = self._buffer[:payload_length]
        elif len(self._buffer) < payload_length:
            self._buffer = bytearray(payload_length)

    def transmit(self, data: Dict[str, Any]) -> None:
        """Transmits the number of bytes to be sent followed by newline,
        then sends a JSON payload

        :param data: The data to send over UART
        :type data: Dict[str, Any]
        """

        payload = json.dumps(data)
        length_info = "{:d}\n".format(len(payload))
        payload = length_info + payload
        payload_bytes = payload.encode("utf-8")
        self._uart.write(payload_bytes)

    def receive(self) -> Dict[str, Any]:
        """Receives a JSON payload and converts it into an object

        :return: An object described by the JSON
        :rtype: Dict[str, Any]
        """

        length_info: bytes = self._uart.readline()
        length = int(length_info.decode("utf-8"))

        self._prepare_buffer(length)
        self._uart.readinto(self._buffer)
        return json.loads(self._buffer.decode("utf-8"))

    @property
    def last_received(self) -> bytearray:
        """The last item received over UART stored in the buffer"""
        return self._buffer

    @property
    def in_waiting(self) -> int:
        """The amount of data waiting in the UART receive pipeline"""
        return self._uart.in_waiting

    @property
    def data_available(self) -> bool:
        """Whether any data is waiting in the UART receive pipeline"""
        return self._uart.in_waiting > 0

    @property
    def connected(self) -> bool:
        """Whether the BLE radio is connected"""
        return self._ble.connected
