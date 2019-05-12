import random
import socket
import string
from datetime import time
from time import time, sleep

from get_data_message import GetDataMessage
from get_headers_message import GetHeadersMessage
from headers_message import HeadersMessage
from inv_message import InvMessage
from message import Message
from obs_notifier import ObsNotifier
from ping_message import PingMessage
from serialize import to_network_addr
from tx_message import TxMessage
from verack_message import VerackMessage
from version_message import VersionMessage


DONATION_ADDRESS = 'bitcoincash:qrg3eyxjm02qsedtj5ev664gyrnxedg0tv0a68hqzw'
notifier = ObsNotifier('localhost', 4444, 'red riding hood')


def main():
    remote_ip = '100.1.209.114'
    version_msg = Message.from_payload(
        b'version',
        VersionMessage(
            version=70015,
            services=0,
            timestamp=int(time()),
            recv_services=1,
            recv_addr=to_network_addr(remote_ip),
            recv_port=8333,
            send_services=0,
            send_addr=to_network_addr('0.0.0.0'),
            send_port=8333,
            nonce=random.randint(0, 2**64),
            user_agent=b'/pyspv:0.0.1/',
            start_height=0,
            relay=True,
        ).serialize(),
    ).serialize()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((remote_ip, 8333))
    sock.send(version_msg)
    while True:
        msg = Message.read_from_stream(sock)
        if msg is None:
            continue
        if msg.header().command() == b'version':
            print(VersionMessage.deserialize(msg.payload()))
        elif msg.header().command() == b'verack':
            sock.send(Message.from_payload(
                command=b'verack',
                payload=VerackMessage().serialize(),
            ).serialize())
            sock.send(Message.from_payload(b'sendheaders', b'').serialize())
            # sock.send(Message.from_payload(
            #     command=b'getheaders',
            #     payload=GetHeadersMessage(
            #         version=70015,
            #         block_locator_hashes=[
            #             bytes.fromhex('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'),
            #         ],
            #         hash_stop=b'\0'*32,
            #     ).serialize()
            # ).serialize())
        elif msg.header().command() == b'ping':
            ping_msg = PingMessage.deserialize(msg.payload())
            sock.send(Message.from_payload(
                command=b'pong',
                payload=PingMessage(ping_msg.nonce()).serialize(),
            ).serialize())
        elif msg.header().command() == b'inv':
            inv_msg = InvMessage.deserialize(msg.payload())
            payload = GetDataMessage(list(inv_msg.inventory())).serialize()
            sock.send(
                Message.from_payload(b'getdata', payload).serialize(),
            )
        elif msg.header().command() == b'headers':
            headers_msg = HeadersMessage.deserialize(msg.payload())
        elif msg.header().command() == b'tx':
            tx_msg = TxMessage.deserialize(msg.payload())
            for output in tx_msg.tx_outputs():
                address = output.address()
                if address is not None \
                        and address.cash_address() == DONATION_ADDRESS:
                    break
            else:
                continue
            print('new donation tx!')
            print(tx_msg)
            memo_bytes = None
            amount = 0
            for output in tx_msg.tx_outputs():
                if output.op_return_payload() is not None:
                    memo_bytes = output.op_return_payload()
                address = output.address()
                if address is not None \
                        and address.cash_address() == DONATION_ADDRESS:
                    amount += output.value()
            print(memo_bytes)
            if memo_bytes is not None:
                try:
                    memo = memo_bytes.decode('utf-8', 'ignore')
                    memo = ''.join(c for c in memo if c in string.printable)
                except Exception as ex:
                    print(ex)
                    memo = None
            else:
                memo = None
            print(memo)
            notifier.notify(amount, memo)


if __name__ == '__main__':
    main()
