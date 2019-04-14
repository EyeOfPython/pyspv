import struct
from io import BytesIO
from typing import List

from serialize import read_var_int


class InvVector:
    FORMAT = 'I32s'

    def __init__(self, type_id: int, hash_bytes: bytes) -> None:
        self._type_id = type_id
        self._hash_bytes = hash_bytes

    def type_id(self) -> int:
        return self._type_id

    def hash_bytes(self) -> bytes:
        return self._hash_bytes

    @classmethod
    def deserialize(cls, payload: bytes) -> 'InvVector':
        return InvVector(*struct.unpack(cls.FORMAT, payload))

    def serialize(self) -> bytes:
        return struct.pack(self.FORMAT, self._type_id, self._hash_bytes)

    def __repr__(self) -> str:
        return f'InvVector(type_id={self._type_id}, hash_bytes={self._hash_bytes})'


class InvMessage:
    def __init__(self, inventory: List[InvVector]) -> None:
        self._inventory = inventory

    @classmethod
    def deserialize(cls, payload: bytes) -> 'InvMessage':
        b = BytesIO(payload)
        inv_count = read_var_int(b)
        inventory = []
        for _ in range(inv_count):
            inv_vector_bytes = b.read(struct.calcsize(InvVector.FORMAT))
            inventory.append(InvVector.deserialize(inv_vector_bytes))
        return InvMessage(inventory)

    def __repr__(self) -> str:
        return f'InvMessage({self._inventory})'
