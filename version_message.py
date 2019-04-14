import struct
import serialize
import io

from serialize import read_var_str


class VersionMessage:
    FORMAT_1 = '<' 'i' 'Qq' 'Q16sH' 'Q16sH' 'Q'
    FORMAT_2 = '<' 'iB'

    def __init__(self,
                 version: int,
                 services: int,
                 timestamp: int,
                 recv_services: int,
                 recv_addr: bytes,
                 recv_port: int,
                 send_services: int,
                 send_addr: bytes,
                 send_port: int,
                 nonce: int,
                 user_agent: bytes,
                 start_height: int,
                 relay: bool,
                 ) -> None:
        self._version = version
        self._services = services
        self._timestamp = timestamp
        self._recv_services = recv_services
        self._recv_addr = recv_addr
        self._recv_port = recv_port
        self._send_services = send_services
        self._send_addr = send_addr
        self._send_port = send_port
        self._nonce = nonce
        self._user_agent = user_agent
        self._start_height = start_height
        self._relay = relay

    @classmethod
    def deserialize(cls, payload: bytes) -> 'VersionMessage':
        b = io.BytesIO(payload)
        part1 = b.read(struct.calcsize(cls.FORMAT_1))
        user_agent = read_var_str(b)
        part2 = b.read(struct.calcsize(cls.FORMAT_2))
        tuple_args = struct.unpack(cls.FORMAT_1, part1) + (user_agent,) + struct.unpack(cls.FORMAT_2, part2)
        return VersionMessage(*tuple_args)

    def serialize(self) -> bytes:
        return struct.pack(
            self.FORMAT_1,
            self._version,
            self._services,
            self._timestamp,
            self._recv_services,
            self._recv_addr,
            self._recv_port,
            self._send_services,
            self._send_addr,
            self._send_port,
            self._nonce,
        ) + serialize.to_var_str(self._user_agent) + struct.pack(
            self.FORMAT_2,
            self._start_height,
            int(self._relay),
        )

    def __repr__(self) -> str:
        return f'''\
VersionMessage(
    version={self._version},
    services={self._services},
    timestamp={self._timestamp},
    recv_services={self._recv_services},
    recv_addr={self._recv_addr},
    recv_port={self._recv_port},
    send_addr={self._send_services},
    send_addr={self._send_addr},
    send_port={self._send_port},
    nonce={self._nonce},
    user_agent={self._user_agent},
    start_height={self._start_height},
    relay={self._relay},
)'''
