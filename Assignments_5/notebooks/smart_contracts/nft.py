from smart_contract import SmartContractDefinition, SmartContractWritingOperation, WritingOperationArguments

class SmartContract():
    
    def __init__(self, name: str, start_mint_timestamp: int, max_token = 10, mint_time: int = 60000):
        self.name = name
        self.token_id = 0
        self.token_owners = {}
        self.max_token = max_token
        self.start_mint_timestamp = start_mint_timestamp
        self.mint_time = mint_time

    def mint(self, operation_arguments: WritingOperationArguments) -> tuple[int, str]:
        if self.token_id >= self.max_token:
            return None, "Maximum number of tokens reached"
        if operation_arguments.timestamp < self.start_mint_timestamp or operation_arguments.timestamp > self.start_mint_timestamp + self.mint_time:
            return None, "Minting is not allowed at this time"
        self.token_id += 1
        self.token_owners[self.token_id] = operation_arguments.issuerPublicKey
        return self.token_id, None
    
    @staticmethod
    def mint_certificate(issuerPublicKey: str, targetSmartContract: SmartContractDefinition) -> SmartContractWritingOperation:
        return SmartContractWritingOperation(issuerPublicKey, targetSmartContract.hash(), "mint")
        
    
    def transfer(self, to: str, token_id: int, operation_arguments: WritingOperationArguments) -> tuple[None , str]:
        if self.token_owners[token_id] == to:
            # raise Exception("You are already the owner of this token")
            # print("You are already the owner of this token")
            return None, "You are already the owner of this token"
        if self.token_owners[token_id] != operation_arguments.issuerPublicKey:
            # raise Exception("You are not the owner of this token")
            # print("You are not the owner of this token")
            return None,  "You are not the owner of this token"
        self.token_owners[token_id] = to
        return None, None
        
    @staticmethod
    def transfer_certificate(issuerPublicKey: str, targetSmartContract: SmartContractDefinition, to: str, token_id: int) -> SmartContractWritingOperation:
        return SmartContractWritingOperation(issuerPublicKey, targetSmartContract.hash(), "transfer", [to, token_id])

    def get_owner(self, token_id: int):
        return self.token_owners[token_id]
    
    def display(self):
        print(f"SmartContract {self.name}:")
        print('Token owners:', [f"{token_id}: {owner[256:264]}" for token_id, owner in self.token_owners.items()])
        print('Start mint timestamp:', self.start_mint_timestamp)
        print('Mint time:', self.mint_time)
        print('Token id:', self.token_id)
        
    def get_nft_icon(self, token_id: int) -> str:
        """Returns a unique Unicode emoji based on token_id"""
        base_unicode = 0x1F400  # Start at 🐀 (Rat emoji)
        return chr(base_unicode + (token_id % 80))  # Cycle through 80 emojis