import struct
from io import BytesIO
from typing import List

from hash import double_sha256
from serialize import read_var_int


class BlockHeader:
    FORMAT = '< i 32s 32s I I I'
    FORMAT_MESSAGE = FORMAT + 'x'

    def __init__(self,
                 version: int,
                 prev_block: bytes,
                 merkle_root: bytes,
                 timestamp: int,
                 bits: int,
                 nonce: int) -> None:
        assert len(prev_block) == 32, f'{len(prev_block)}'
        assert len(merkle_root) == 32
        self._version = version
        self._prev_block = prev_block
        self._merkle_root = merkle_root
        self._timestamp = timestamp
        self._bits = bits
        self._nonce = nonce

    @classmethod
    def deserialize(cls, payload: bytes) -> 'BlockHeader':
        return BlockHeader(
            *struct.unpack(cls.FORMAT_MESSAGE, payload)
        )

    def block_hash(self) -> bytes:
        return double_sha256(self.serialize())

    def bits(self) -> int:
        return self._bits

    def target(self) -> int:
        exp = (0xff00_0000 & self._bits) >> (3 * 8)
        mantissa = 0x00ff_ffff & self._bits
        return mantissa * (1 << (8 * (exp - 3)))

    def prev_block_hash(self) -> bytes:
        return self._prev_block

    def serialize(self) -> bytes:
        return struct.pack(
            self.FORMAT,
            self._version,
            self._prev_block,
            self._merkle_root,
            self._timestamp,
            self._bits,
            self._nonce,
        )

    def __repr__(self) -> str:
        return f'''\
BlockHeader(
    version={self._version},
    prev_block={self._prev_block},
    merkle_root={self._merkle_root},
    timestamp={self._timestamp},
    bits={self._bits},
    nonce={self._nonce},
), hash={self.block_hash()}'''


class HeadersMessage:
    def __init__(self, headers: List[BlockHeader]) -> None:
        self._headers = headers

    @classmethod
    def deserialize(cls, payload: bytes) -> 'HeadersMessage':
        b = BytesIO(payload)
        header_count = read_var_int(b)
        headers = []
        for _ in range(header_count):
            headers.append(
                BlockHeader.deserialize(
                    b.read(struct.calcsize(BlockHeader.FORMAT_MESSAGE))
                )
            )
        return HeadersMessage(headers)

    def __repr__(self) -> str:
        return f'HeadersMessage({self._headers})'
