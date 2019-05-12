import struct
from io import BytesIO
from typing import List, BinaryIO, Optional, Iterable
import re
from cashaddress.convert import Address

from serialize import read_var_int
import bitcoinpython

class TxInput:
    OUTPOINT_FORMAT = '< 32s I'
    SEQUENCE_FORMAT = '< I'

    def __init__(self,
                 prev_tx_output: bytes,
                 prev_tx_output_idx: int,
                 sig_script: bytes,
                 sequence: int) -> None:
        self._prev_tx_output = prev_tx_output
        self._prev_tx_output_idx = prev_tx_output_idx
        self._sig_script = sig_script
        self._sequence = sequence

    @classmethod
    def read_from_file(cls, file: BinaryIO) -> 'TxInput':
        prev_tx_output, prev_tx_output_idx = struct.unpack(
            cls.OUTPOINT_FORMAT,
            file.read(struct.calcsize(cls.OUTPOINT_FORMAT)),
        )
        sig_script_len = read_var_int(file)
        sig_script = file.read(sig_script_len)
        sequence, = struct.unpack(
            cls.SEQUENCE_FORMAT,
            file.read(struct.calcsize(cls.SEQUENCE_FORMAT)),
        )
        return TxInput(
            prev_tx_output=prev_tx_output,
            prev_tx_output_idx=prev_tx_output_idx,
            sig_script=sig_script,
            sequence=sequence,
        )

    def __repr__(self) -> str:
        return f'''\
TxInput(
    prev_tx_output={self._prev_tx_output},
    prev_tx_output_idx={self._prev_tx_output_idx},
    sig_script={self._sig_script},
    sequence={self._sequence},
)
'''


class TxOutput:
    VALUE_FORMAT = '< Q'

    # OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
    REG_P2PKH = re.compile(
        b'\x76\xa9.*?(?P<address>.{20})\x88\xac',
        re.DOTALL,
    )
    REG_OP_RETURN = re.compile(
        b'\x6a(?P<payload>.*)',
        re.DOTALL,
    )

    def __init__(self,
                 value: int,
                 pub_key_script: bytes) -> None:
        self._value = value
        self._pub_key_script = pub_key_script

    @classmethod
    def read_from_file(cls, file: BinaryIO) -> 'TxOutput':
        value, = struct.unpack(
            cls.VALUE_FORMAT,
            file.read(struct.calcsize(cls.VALUE_FORMAT)),
        )
        pub_key_script_len = read_var_int(file)
        pub_key_script = file.read(pub_key_script_len)
        return TxOutput(
            value=value,
            pub_key_script=pub_key_script,
        )

    def address(self) -> Optional[Address]:
        match = self.REG_P2PKH.match(self._pub_key_script)
        if match is None:
            return None
        return Address('P2PKH', list(match.group('address')))

    def op_return_payload(self) -> Optional[bytes]:
        match = self.REG_OP_RETURN.match(self._pub_key_script)
        if match is None:
            return None
        return match.group('payload')

    def pub_key_script(self) -> bytes:
        return self._pub_key_script

    def value(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f'TxOutput(value={self._value}, pub_key_script={self._pub_key_script})'


class TxMessage:
    VERSION_FORMAT = '< i'
    LOCK_TIME_FORMAT = '< I'

    def __init__(self,
                 version: int,
                 tx_inputs: List[TxInput],
                 tx_outputs: List[TxOutput],
                 lock_time: int) -> None:
        self._version = version
        self._tx_inputs = tx_inputs
        self._tx_outputs = tx_outputs
        self._lock_time = lock_time

    @classmethod
    def deserialize(cls, payload: bytes) -> 'TxMessage':
        b = BytesIO(payload)

        version, = struct.unpack(
            cls.VERSION_FORMAT,
            b.read(struct.calcsize(cls.VERSION_FORMAT)),
        )
        tx_in_count = read_var_int(b)
        tx_inputs = []
        for _ in range(tx_in_count):
            tx_inputs.append(TxInput.read_from_file(b))
        tx_out_count = read_var_int(b)
        tx_outputs = []
        for _ in range(tx_out_count):
            tx_outputs.append(TxOutput.read_from_file(b))
        lock_time, = struct.unpack(
            cls.LOCK_TIME_FORMAT,
            b.read(struct.calcsize(cls.LOCK_TIME_FORMAT)),
        )
        return TxMessage(
            version=version,
            tx_inputs=tx_inputs,
            tx_outputs=tx_outputs,
            lock_time=lock_time,
        )

    def __repr__(self) -> str:
        return f'''\
TxMessage(
    version={self._version},
    tx_inputs={self._tx_inputs},
    tx_outputs={self._tx_outputs},
    lock_time={self._lock_time},
)
'''

    def tx_outputs(self) -> Iterable[TxOutput]:
        return iter(self._tx_outputs)
