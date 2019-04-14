import struct


class PingMessage:
    FORMAT = '>Q'

    def __init__(self, nonce: int) -> None:
        self._nonce = nonce

    @classmethod
    def deserialize(cls, payload: bytes) -> 'PingMessage':
        nonce, = struct.unpack(cls.FORMAT, payload)
        return PingMessage(nonce)

    def nonce(self) -> int:
        return self._nonce

    def serialize(self) -> bytes:
        return struct.pack(self.FORMAT, self._nonce)
