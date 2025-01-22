from typing import List
from certificate import Certificate

class Block(Certificate):
    indexInBlockchain: int
    parentBlockHash: str
    certificateList: List[Certificate]

    def __init__(self, issuerPublicKey: str, indexInBlockchain: int, parentBlockHash: str, certificateList: List[Certificate]):
        super().__init__(issuerPublicKey)
        self.indexInBlockchain = indexInBlockchain
        self.parentBlockHash = parentBlockHash
        self.certificateList = certificateList
        
    def build_payload(self):
        payload = super().build_payload()
        payload['indexInBlockchain'] = self.indexInBlockchain
        payload['parentBlockHash'] = self.parentBlockHash
        payload['certificateList'] = [certificate.build_payload() for certificate in self.certificateList]
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
        print()