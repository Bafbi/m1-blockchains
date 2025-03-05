from typing import List
from certificate import Certificate
from helpers import timestamp

class Block(Certificate):
    indexInBlockchain: int
    parentBlockHash: str
    certificateList: List[Certificate]
    nonce: int

    def __init__(self, issuerPublicKey: str, indexInBlockchain: int, parentBlockHash: str, certificateList: List[Certificate], nonce: int = 0, timestamp: int = None):
        super().__init__(issuerPublicKey, timestamp=timestamp)
        self.indexInBlockchain = indexInBlockchain
        if not isinstance(parentBlockHash, str):
            raise ValueError('Parent block hash must be a string')
        self.parentBlockHash = parentBlockHash
        self.certificateList = certificateList
        self.nonce = nonce
        
    def build_payload(self):
        payload = super().build_payload()
        payload['indexInBlockchain'] = self.indexInBlockchain
        payload['parentBlockHash'] = self.parentBlockHash
        payload['certificateList'] = [certificate.build_payload() for certificate in self.certificateList]
        payload['nonce'] = self.nonce
        return payload
    
    def is_legit(self):
        return super().is_legit() and all([certificate.is_legit() for certificate in self.certificateList])

    def display(self):
        super().display()
        print('Index in blockchain:', self.indexInBlockchain)
        print('Parent block hash:', self.parentBlockHash)
        print('Certificate list:')
        for certificate in self.certificateList:
            certificate.display()
            print('---')
        print()