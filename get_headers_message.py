import struct
from typing import List

from serialize import to_var_int


class GetHeadersMessage:
    def __init__(self,
                 version: int,
                 block_locator_hashes: List[bytes],
                 hash_stop: bytes) -> None:
        self._version = version
        self._block_locator_hashes = block_locator_hashes
        self._hash_stop = hash_stop

    def serialize(self) -> bytes:
        byte_arr = bytearray()
        byte_arr.extend(struct.pack('>I', self._version))
        byte_arr.extend(to_var_int(len(self._block_locator_hashes)))
        for block_locator_hash in self._block_locator_hashes:
            byte_arr.extend(block_locator_hash)
        byte_arr.extend(self._hash_stop)
        return byte_arr
