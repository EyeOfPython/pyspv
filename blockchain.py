from typing import Optional, Dict

from headers_message import BlockHeader


GENESIS_BLOCK = BlockHeader(
    version=1,
    prev_block=b'\0'*32,
    merkle_root=bytes.fromhex(
        '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b'
    )[::-1],
    timestamp=1231006505,
    bits=0x1d00ffff,
    nonce=2083236893,
)


class Block:
    def __init__(self,
                 block_header: BlockHeader,
                 previous_block: Optional['Block'],
                 block_height: int) -> None:
        self._block_header = block_header
        self._previous_block = previous_block
        self._block_height = block_height

    def block_header(self) -> BlockHeader:
        return self._block_header

    def previous_block(self) -> Optional['Block']:
        return self._previous_block

    def block_height(self) -> int:
        return self._block_height + 1


class Blockchain:
    def __init__(self) -> None:
        self._blocks: Dict[bytes, Block] = ...  # [GENESIS_BLOCK]
        self._tips = [GENESIS_BLOCK.block_hash()]

    def receive_header(self, block: BlockHeader) -> bool:
        block.target()
        hash_int = int.from_bytes(block.block_hash(), 'little')
        if hash_int > block.target():
            return False
        if block.block_hash() in self._blocks:
            return True
        for i, tip in enumerate(self._tips):
            current_block = self._blocks[tip]
            for n in range(15):
                if current_block.block_header().block_hash() == block.prev_block_hash():
                    self._tips[i] = block.block_hash()
                    self._blocks[block.block_hash()] = Block(
                        block,
                        current_block,
                        current_block.block_height() + 1,
                    )
                    return True
                else:
                    current_block = current_block.previous_block()


if __name__ == '__main__':
    print(GENESIS_BLOCK)
    h = GENESIS_BLOCK.serialize().hex()
    print(*[h[i*16:i*16+16] for i in range(160 // 16)], sep='\n')
    print(hex(GENESIS_BLOCK.target()))

    blockchain = Blockchain()
    print(blockchain.receive_header(GENESIS_BLOCK))
