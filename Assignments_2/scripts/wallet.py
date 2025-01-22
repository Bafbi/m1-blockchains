from helpers import cryptography
from certificate import Certificate

class Wallet:
    publicKey: str
    privateKey: str

    def __init__(self):
        self.privateKey = cryptography.generate_random_private_key()
        self.publicKey = cryptography.get_public_key_from_private_key(self.privateKey)

    def sign(self, certificate: Certificate):
        certificate.signature = cryptography.sign_hash_with_private_key(certificate.hash(), self.privateKey)

    def display(self):
        print('Public key:', self.publicKey)
        print('Private key:', self.privateKey)
        print()