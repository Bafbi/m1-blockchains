from json import dumps
from helpers import cryptography


class RaffleTicket():
    ownerPublicKey: str
    number: int
    raffleHash: str

    def __init__(self, ownerPublicKey: str, number: int, raffleHash: str):
        self.ownerPublicKey = ownerPublicKey
        self.number = number
        self.raffleHash = raffleHash

    def build_payload(self):
        return {
            'ownerPublicKey': self.ownerPublicKey,
            'number': self.number,
            'raffleHash': self.raffleHash
        }
    
    def hash(self):
        return cryptography.hash_string(dumps(self.build_payload(), sort_keys=True))