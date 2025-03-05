from typing import List
from smart_contract import SmartContractDefinition, SmartContractWritingOperation, WritingOperationArguments



class SmartContract():
    
    class ItemInfo():
        def __init__(self, name: str, description: str, price: int):
            self.name = name
            self.description = description
            self.price = price
    
    class MarketItem():
        def __init__(self, itemInfo, ownerPublicKey: str):
            self.itemInfo = itemInfo
            self.ownerPublicKey = ownerPublicKey
    
    def __init__(self):
        self.market: List[Self.MarketItem] = [] # type: ignore

    def add_item(self, itemInfo, operation_arguments: WritingOperationArguments):
        self.market.append(self.MarketItem(itemInfo, operation_arguments.issuerPublicKey))
    
    @staticmethod
    def add_item_certificate(issuerPublicKey: str, targetSmartContract: SmartContractDefinition, itemInfo) -> SmartContractWritingOperation:
        return SmartContractWritingOperation(issuerPublicKey, targetSmartContract.hash(), "add_item", [itemInfo])
    
    def display(self):
        print('Market items:', [(item.itemInfo.name, item.itemInfo.description, item.itemInfo.price, item.ownerPublicKey[256:264]) for item in self.market])