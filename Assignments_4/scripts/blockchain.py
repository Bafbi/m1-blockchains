from typing import List

from block import Block
from certificate import Certificate
from helpers import cryptography


class Blockchain:
    blockList: List[Block]

    def __init__(self):
        self.blockList = [Block(cryptography.get_black_hole_public_key(), 0, cryptography.get_default_hash(), [], timestamp=0)]

    def get_latest_block(self) -> Block:
        return self.blockList[-1]
    
    def is_legit(self):
        return all([block.is_legit() for block in self.blockList])
    
    def contains_certificate(self, certificate: Certificate):
        if any([certificate == block for block in self.blockList]):
            return True
        if any([certificate in block.certificateList for block in self.blockList]):
            return True
        return False
    
    def display(self):
        for block in self.blockList:
            block.display()
            print('----------------------------------')

    def __eq__(self, value):
        return isinstance(value, Blockchain) and self.blockList == value.blockList
        