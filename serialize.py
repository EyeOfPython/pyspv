from typing import BinaryIO


def to_var_int(number: int) -> bytes:
    if number < 0:
        raise ValueError('Number must be unsigned')
    elif number < 0xfd:
        return number.to_bytes(1, 'little')
    elif number <= 0xffff:
        return b'\xfd' + number.to_bytes(2, 'little')
    elif number <= 0xffff_ffff:
        return b'\xfe' + number.to_bytes(4, 'little')
    else:
        return b'\xff' + number.to_bytes(8, 'little')


def to_var_str(data: bytes) -> bytes:
    return to_var_int(len(data)) + data


def to_network_addr(ip: str) -> bytes:
    ip_hex = '%02x%02x%02x%02x' % tuple(map(int, ip.split('.')))
    return bytes.fromhex('00' * 10 + 'ffff' + ip_hex)


def read_var_int(b: BinaryIO) -> int:
    first_byte = b.read(1)[0]
    if first_byte < 0xfd:
        return first_byte
    elif first_byte == 0xfd:
        return int.from_bytes(b.read(2), 'little')
    elif first_byte == 0xfe:
        return int.from_bytes(b.read(4), 'little')
    elif first_byte == 0xff:
        return int.from_bytes(b.read(8), 'little')


def read_var_str(b: BinaryIO) -> bytes:
    str_len = read_var_int(b)
    return b.read(str_len)
