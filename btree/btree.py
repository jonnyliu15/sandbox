from btree.uint64 import uint64
from enum import Enum

HEADER = 4
PAGE_SIZE = 4096
MAX_KEY_SIZE = 1000
MAX_VAL_SIZE = 3000


class BTreeConfig:
    HEADER: int = 4
    PAGE_SIZE: int = 4096
    MAX_KEY_SIZE: int = 1000
    MAX_VAL_SIZE: int = 3000


class BTreeNodeType(Enum):
    INTERNAL = 0
    LEAF = 1


class BTreeNode:
    data: bytearray

    def __init__(self) -> None:
        self.data = bytearray(PAGE_SIZE)

    @property
    def type(self) -> BTreeNodeType:
        return BTreeNodeType(uint64.from_bytearray(self.data[0:2]).value)

    @property
    def number_of_keys(self) -> int:
        return uint64.from_bytearray(self.data[2:4]).value

    def set_header(self, type: BTreeNodeType, number_of_keys: int) -> None:
        assert number_of_keys >= 0 and number_of_keys <= 65535
        self.data[0:2] = uint64(type.value).to_bytearray(2)
        self.data[2:4] = uint64(number_of_keys).to_bytearray(2)

    def get_ptr(self, index: int) -> uint64:
        assert index >= 0 and index < self.number_of_keys
        position = HEADER + 8 * index
        return uint64.from_bytearray(self.data[position : position + 8])

    def set_ptr(self, index: int, ptr: uint64) -> None:
        assert index >= 0 and index < self.number_of_keys
        position = HEADER + 8 * index
        self.data[position : position + 8] = ptr.to_bytearray(8)

    def get_offset(self, index: int) -> int:
        assert index >= 0 and index < self.number_of_keys
        # the first KV pair is always at position 0, so its offset doesn't need to be stored within the offset list
        if index == 0:
            return 0
        offset_pos = (
            HEADER + 8 * self.number_of_keys + 2 * self.number_of_keys + 2 * (index - 1)
        )
        return uint64.from_bytearray(self.data[offset_pos : offset_pos + 2]).value

    def set_offset(self, index: int, offset: int) -> None:
        assert index > 0 and index < self.number_of_keys
        assert offset > 0 and offset < 65536
        offset_pos = (
            HEADER + 8 * self.number_of_keys + 2 * self.number_of_keys + 2 * (index - 1)
        )
        self.data[offset_pos : offset_pos + 2] = uint64(offset).to_bytearray(2)

    def get_key(self, index: int) -> bytearray:
        assert index >= 0 and index < self.number_of_keys
        kv_pair_position = (
            HEADER
            + 8 * self.number_of_keys
            + 2 * self.number_of_keys
            + self.get_offset(index)
        )
        key_length = uint64.from_bytearray(
            self.data[kv_pair_position : kv_pair_position + 2]
        ).value
        return self.data[kv_pair_position + 4 : kv_pair_position + 4 + key_length]

    def get_value(self, index: int) -> bytearray:
        assert index >= 0 and index < self.number_of_keys
        kv_pair_position = (
            HEADER
            + 8 * self.number_of_keys
            + 2 * self.number_of_keys
            + self.get_offset(index)
        )
        key_length = uint64.from_bytearray(
            self.data[kv_pair_position : kv_pair_position + 2]
        ).value
        value_length = uint64.from_bytearray(
            self.data[kv_pair_position + 2 : kv_pair_position + 4]
        ).value
        return self.data[
            kv_pair_position
            + 4
            + key_length : kv_pair_position
            + 4
            + key_length
            + value_length
        ]

    @property
    def size(self) -> int:
        return (
            HEADER
            + 8 * self.number_of_keys
            + 2 * self.number_of_keys
            + self.get_offset(self.number_of_keys)
        )


class BTree:
    root: uint64

    def __init__(self) -> None:
        raise NotImplementedError

    def insert(self, node: BTreeNode) -> None:
        raise NotImplementedError

    def get(self, key: int) -> BTreeNode:
        raise NotImplementedError
