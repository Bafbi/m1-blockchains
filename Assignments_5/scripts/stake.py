from typing import Dict, List
from certificate import Certificate
from block import Block


class StakingOperation(Certificate):
    tokenAmount: int
    
    def __init__(self, issuerPublicKey: str, tokenAmount: int):
        super().__init__(issuerPublicKey)
        self.tokenAmount = tokenAmount
    
    def build_payload(self) -> Dict[str, int]:
        payload = super().build_payload()
        payload['tokenAmount'] = self.tokenAmount
        return payload
    
    @staticmethod
    def build_staking_accounts(blockList: List[Block]) -> Dict[str, int]:
        stakingAccounts = {}
        for block in blockList:
            for certificate in block.certificateList:
                if not isinstance(certificate, StakingOperation):
                    continue
                if certificate.issuerPublicKey not in stakingAccounts:
                    stakingAccounts[certificate.issuerPublicKey] = 0
                stakingAccounts[certificate.issuerPublicKey] += certificate.tokenAmount
        return stakingAccounts