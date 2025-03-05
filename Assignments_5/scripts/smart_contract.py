from typing import List
from blockchain import Blockchain
from certificate import Certificate


class SmartContractDefinition(Certificate):
    sourceCode: str
    classArgumentList: List[any]
    
    def __init__(self, issuerPublicKey: str, sourceCode: str, classArgumentList: List[any] = []):
        super().__init__(issuerPublicKey)
        self.sourceCode = sourceCode
        self.classArgumentList = classArgumentList
        
    def build_payload(self):
        payload = super().build_payload()
        payload['sourceCode'] = self.sourceCode
        return payload
    
    def instantiate_contract(self):
        exec_local = {}
        exec(self.sourceCode, locals=exec_local)
        return exec_local["SmartContract"](*self.classArgumentList)

    @staticmethod
    def get_smart_contract_at_current_state(blockchain: Blockchain, targetSmartContractHash: str):
        operations = []
        smartContractDef = None
        for certificate in blockchain.iterate_certificates():
            if isinstance(certificate, SmartContractDefinition) and certificate.hash() == targetSmartContractHash:
                smartContractDef = certificate
                continue
            if isinstance(certificate, SmartContractWritingOperation) and certificate.targetSmartContractHash == targetSmartContractHash:
                operations.append(certificate)
                continue
        # print(f"operations: {operations}")
        smartContract = smartContractDef.instantiate_contract()
        for operation in sorted(filter(lambda x: x.timestamp > smartContractDef.timestamp, operations), key=lambda x: x.timestamp):
            operation.apply_on_contract(smartContract)
        
        return smartContract
    
    # @staticmethod
    # def get_smart_contract_at_tmp_state(blockchain: Blockchain, targetSmartContractHash: str, tmp_certificate: List[Certificate]):
    #     operations = [operation for operation in tmp_certificate if isinstance(operation, SmartContractWritingOperation) and operation.targetSmartContractHash == targetSmartContractHash]
    #     smartContract = SmartContractDefinition.get_smart_contract_at_current_state(blockchain, targetSmartContractHash)
    #     for operation in sorted(operations, key=lambda x: x.timestamp):
    #         operation.apply_on_contract(smartContract)
    #     return smartContract
    
    
class WritingOperationArguments():
    def __init__(self, issuerPublicKey: str, timestamp: int):
        self.issuerPublicKey = issuerPublicKey
        self.timestamp = timestamp
        
    
class SmartContractWritingOperation(Certificate):
    targetSmartContractHash: str
    targetFunctionName: str
    functionArgumentList: List[any]
    
    def __init__(self, issuerPublicKey: str, targetSmartContractHash: str, targetFunctionName: str, functionArgumentList: List[any] = []):
        super().__init__(issuerPublicKey)
        self.targetSmartContractHash = targetSmartContractHash
        self.targetFunctionName = targetFunctionName
        self.functionArgumentList = functionArgumentList
    
    def build_payload(self):
        payload = super().build_payload()
        payload['targetSmartContractHash'] = self.targetSmartContractHash
        payload['targetFunctionName'] = self.targetFunctionName
        payload['functionArgumentList'] = self.functionArgumentList
        return payload
    
    def apply_on_contract(self, contractPythonObject):
        # print(f"applying operation {self.targetFunctionName} on contract {contractPythonObject}, as {self.issuerPublicKey[256:264]}, at {self.timestamp}")
        args = WritingOperationArguments(self.issuerPublicKey, self.timestamp)
        return getattr(contractPythonObject, self.targetFunctionName)(*self.functionArgumentList, operation_arguments=args)