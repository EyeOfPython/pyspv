from typing import List

from inv_message import InvVector
from serialize import to_var_int


class GetDataMessage:
    def __init__(self, inventory: List[InvVector]) -> None:
        self._inventory = inventory

    def serialize(self) -> bytes:
        b = bytearray()
        b.extend(to_var_int(len(self._inventory)))
        for inv in self._inventory:
            b.extend(inv.serialize())
        return bytes(b)
