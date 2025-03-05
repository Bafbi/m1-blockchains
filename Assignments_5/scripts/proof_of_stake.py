from typing import List
from block import Block
from blockchain import Blockchain
from helpers import cryptography
from stake import StakingOperation
from ticket import RaffleTicket


class ProofOfStake():
    defaultForgerPublicKey: str

    def __init__(self, defaultForgerPublicKey: str):
        self.defaultForgerPublicKey = defaultForgerPublicKey

    def hash_distance(self, hash1: str, hash2: str):
        return abs(int(hash1, 16) - int(hash2, 16))
    
    def get_next_forger_public_key(self, blockList: List[Block]) -> str:
        stakingAccounts = StakingOperation.build_staking_accounts(blockList)
        if len(stakingAccounts) == 0:
            return self.defaultForgerPublicKey
        minDistance = int('f' * 64, 16)
        ticketCreated = 0
        raffleHash = blockList[-1].hash()
        for publicKey, stake in stakingAccounts.items():
            for _ in range(int(stake)):
                ticket = RaffleTicket(publicKey, ticketCreated, raffleHash)
                ticketCreated += 1
                distance = self.hash_distance(ticket.hash(), blockList[-1].hash())
                if distance < minDistance:
                    forgerPublicKey = publicKey
                    minDistance = distance
        return forgerPublicKey
    
    def is_next_block_forger_legit(self, blockList: List[Block], nextBlock: Block) -> bool:
        return nextBlock.issuerPublicKey == self.get_next_forger_public_key(blockList)
    
    def is_blockchain_legit(self, blockchain: Blockchain) -> bool:
        blockList = blockchain.blockList.copy()
        blockList.pop(0)
        while len(blockList) > 1:
            block = blockList.pop()
            if not self.is_next_block_forger_legit(blockList, block):
                return False
        return True