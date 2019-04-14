import random
import socket
from datetime import time
from time import time, sleep

from get_headers_message import GetHeadersMessage
from headers_message import HeadersMessage
from inv_message import InvMessage
from message import Message
from ping_message import PingMessage
from serialize import to_network_addr
from verack_message import VerackMessage
from version_message import VersionMessage

block_headers = []

if __name__ == '__main__':
    remote_ip = '100.1.209.114'
    # remote_ip = 'let.cash'
    # remote_ip = '54.167.105.231'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((remote_ip, 8333))
    sock.send(
        Message.from_payload(
            b'version',
            VersionMessage(
                version=70015,
                services=0,
                timestamp=int(time()),
                recv_services=1,
                recv_addr=to_network_addr(remote_ip),
                recv_port=8333,
                send_services=0,
                send_addr=to_network_addr('46.5.253.233'),
                send_port=8333,
                nonce=random.randint(0, 2**64),
                user_agent=b'/pyspv:0.0.1/',
                start_height=0,
                relay=False,
            ).serialize(),
        ).serialize(),
    )
    while True:
        msg = Message.read_from_stream(sock)
        if msg is None:
            continue
        print(repr(msg))
        if msg.header().command() == b'version':
            print(VersionMessage.deserialize(msg.payload()))
        elif msg.header().command() == b'verack':
            sock.send(Message.from_payload(
                command=b'verack',
                payload=VerackMessage().serialize(),
            ).serialize())
            sock.send(Message.from_payload(b'sendheaders', b'').serialize())
            sock.send(Message.from_payload(
                command=b'getheaders',
                payload=GetHeadersMessage(
                    version=70015,
                    block_locator_hashes=[
                        bytes.fromhex('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'),
                    ],
                    hash_stop=b'\0'*32,
                ).serialize()
            ).serialize())
        elif msg.header().command() == b'ping':
            ping_msg = PingMessage.deserialize(msg.payload())
            sock.send(Message.from_payload(
                command=b'pong',
                payload=PingMessage(ping_msg.nonce()).serialize(),
            ).serialize())
        elif msg.header().command() == b'inv':
            inv_msg = InvMessage.deserialize(msg.payload())
            print(inv_msg)
        elif msg.header().command() == b'headers':
            headers_msg = HeadersMessage.deserialize(msg.payload())

