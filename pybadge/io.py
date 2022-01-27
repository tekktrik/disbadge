import board
from micropython import const
from keypad import ShiftRegisterKeys, Event


class IOManager:
    def __init__(self):

        self._pad = ShiftRegisterKeys(
            clock=board.BUTTON_CLOCK,
            data=board.BUTTON_OUT,
            latch=board.BUTTON_LATCH,
            key_count=8,
            value_when_pressed=True,
            interval=0.1,
            max_events=1,
        )

        self._event = Event(8)

    def update_inputs(self) -> bool:
        self._pad.events.get_into(self._event)
        if self._event.released:
            self._event = Event(8)
            return False
        return True

    @property
    def button_pressed(self) -> int:
        return self._event.key_number
