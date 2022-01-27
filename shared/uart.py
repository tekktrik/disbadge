import json

try:
    from typing import Dict, Any, Optional, Type
    from types import TracebackType
    from adafruit_ble.services.nordic import UARTService
    from adafruit_ble import BLERadio
except ImportError:
    pass


class UARTManager:
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
        """

        payload = json.dumps(data)
        length_info = "{:d}\n".format(len(payload))
        payload = length_info + payload
        payload_bytes = payload.encode("utf-8")
        self._uart.write(payload_bytes)

    def receive(self) -> Dict[str, Any]:
        length_info: bytes = self._uart.readline()
        length = int(length_info.decode("utf-8"))

        self._prepare_buffer(length)
        self._uart.readinto(self._buffer)
        return json.loads(self._buffer.decode("utf-8"))

    @property
    def last_received(self) -> bytearray:
        return self._buffer

    @property
    def data_available(self) -> int:
        return self._uart.in_waiting

    @property
    def connected(self) -> bool:
        return self._ble.connected
