from typing import Self
from enum import Enum


class ByteOrder(Enum):
    BIG_ENDIAN = "big"
    LITTLE_ENDIAN = "little"


class uint64:
    _value: int

    def __init__(self, value: int) -> None:
        if value < 0:
            raise ValueError("Value must be greater than or equal to 0")
        if value > 18446744073709551615:
            raise ValueError("Value must be less than or equal to 18446744073709551615")
        self._value = value

    @staticmethod
    def from_bytearray(data: bytearray, order=ByteOrder.LITTLE_ENDIAN) -> Self:
        return uint64(int.from_bytes(data, order.value))

    def to_bytearray(self, length: int, order=ByteOrder.LITTLE_ENDIAN) -> bytearray:
        return self._value.to_bytes(length, order.value)

    @property
    def value(self) -> int:
        return self._value
