import hashlib


def double_sha256(msg: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(msg).digest()).digest()


if __name__ == '__main__':
    print(double_sha256(b''))
