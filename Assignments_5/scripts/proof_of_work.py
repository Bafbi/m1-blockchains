from typing import List
from block import Block
from blockchain import Blockchain


class ProofOfWork:
    difficulty: int

    def __init__(self, difficulty: int = 3):

        self.difficulty = difficulty

    def solve_puzzle(self, block: Block) -> Block:
        nbTry = 0
        while not block.hash()[:self.difficulty] == '0' * self.difficulty:
            nbTry += 1
            if nbTry % 1000 == 0:
                # a nice updating visual
                print(f"Try {nbTry} - {block.hash()}", end='\r')
            block.nonce += 1
        print(f"Try {nbTry} - {block.hash()}")
        return block
    
    def is_next_block_forger_legit(self, blockList: List[Block], nextBlock: Block) -> bool:
        return nextBlock.hash()[:self.difficulty] == '0' * self.difficulty and nextBlock.parentBlockHash == blockList[-1].hash()
    
    def is_blockchain_legit(self, blockchain: Blockchain) -> bool:
        blockList = blockchain.blockList.copy()
        blockList.pop(0)
        while len(blockList) > 1:
            block = blockList.pop()
            if not self.is_next_block_forger_legit(blockList, block):
                return False
        return True