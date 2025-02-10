from typing import Self
from helpers import timestamp as timestamp_helper
from helpers import cryptography

class Certificate:
    issuerPublicKey: str
    signature: str
    timestamp: int

    def __init__(self, issuerPublicKey: str, signature: str = None, timestamp: int = None):
        self.issuerPublicKey = issuerPublicKey
        self.signature = signature
        self.timestamp = timestamp if timestamp != None else timestamp_helper.now()
        
    def build_payload(self):
        return {
            'issuerPublicKey': self.issuerPublicKey,
            'timestamp': self.timestamp
        }

    def hash(self):
        return cryptography.hash_string(str(self.build_payload()))
    
    def equals(self, certificate: Self):
        return self.hash() == certificate.hash()
    
    def is_legit(self):
        # print( self.issuerPublicKey, self.signature, self.hash() )
        # if genesis block then return True
        if self.issuerPublicKey == cryptography.get_black_hole_public_key():
            return True
        return cryptography.has_public_key_signed_this_hash(self.issuerPublicKey, self.signature,self.hash() )
    
    def display(self):
        print('Issuer public key:', self.issuerPublicKey)
        print('Signature:', self.signature)
        print('Timestamp:', self.timestamp)
        print('Hash:', self.hash())
        print('Is legit:', self.is_legit())

    def __hash__(self):
        return int(self.hash(), 16)

    def __eq__(self, value: Self):
        return self.equals(value)