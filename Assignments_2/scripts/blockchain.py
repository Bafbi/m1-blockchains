from typing import List

from block import Block
from helpers import cryptography


class Blockchain:
    blockList: List[Block]

    def __init__(self):
        self.blockList = [Block(cryptography.get_black_hole_public_key(), 0, cryptography.get_default_hash(), [])]

    def get_latest_block(self) -> Block:
        return self.blockList[-1]
    
    def is_legit(self):
        return all([block.is_legit() for block in self.blockList])
    
    def display(self):
        for block in self.blockList:
            block.display()
            print()
        