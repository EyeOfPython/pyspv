import socket
import struct
from typing import Optional

from hash import double_sha256


class MessageHeader:
    FORMAT = '<4s12sI4s'
    MAGIC = bytes.fromhex('e3e1f3e8')

    def __init__(self, command: bytes, payload_size: int, checksum: bytes) -> None:
        assert len(command) <= 12
        self._command = command
        self._payload_size = payload_size
        self._checksum = checksum

    @classmethod
    def read_from_stream(cls, stream: socket.socket) -> Optional['MessageHeader']:
        header_data = stream.recv(struct.calcsize(cls.FORMAT))
        if not header_data:
            return None
        magic, command, payload_size, checksum = struct.unpack(
            cls.FORMAT,
            header_data,
        )
        assert magic == cls.MAGIC
        return MessageHeader(
            command.rstrip(b'\0'),
            payload_size,
            checksum,
        )

    def command(self) -> bytes:
        return self._command

    def payload_size(self) -> int:
        return self._payload_size

    def checksum(self) -> bytes:
        return self._checksum

    def serialize(self) -> bytes:
        return struct.pack(
            self.FORMAT,
            self.MAGIC,
            self._command.ljust(12, b'\0'),
            self._payload_size,
            self._checksum,
        )

    def __repr__(self) -> str:
        return f'MessageHeader({self._command}, {self._payload_size}, {self._checksum})'


class Message:
    def __init__(self, header: MessageHeader, payload: bytes) -> None:
        self._header = header
        self._payload = payload

    @classmethod
    def from_payload(cls, command: bytes, payload: bytes) -> 'Message':
        return Message(
            MessageHeader(
                command,
                len(payload),
                double_sha256(payload)[:4],
            ),
            payload,
        )

    @classmethod
    def read_from_stream(cls, stream: socket.socket) -> Optional['Message']:
        header = MessageHeader.read_from_stream(stream)
        if header is None:
            return None
        payload = bytearray()
        while len(payload) < header.payload_size():
            payload.extend(stream.recv(header.payload_size() - len(payload)))
        checksum = double_sha256(payload)[:4]
        assert header.checksum() == checksum
        return Message(header, bytes(payload))

    def serialize(self) -> bytes:
        return self._header.serialize() + self._payload

    def header(self) -> MessageHeader:
        return self._header

    def payload(self) -> bytes:
        return self._payload

    def __repr__(self) -> str:
        return f'Message({self._header}, {self._payload})'
