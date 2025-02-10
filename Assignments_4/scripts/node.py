from block import Block
from blockchain import Blockchain
from certificate import Certificate
from network import Node
from proof_of_stake import ProofOfStake
from wallet import Wallet

class BlockchainNode(Node):
    wallet: Wallet
    #consensusAlgorithm
    blockchain: Blockchain

    def __init__(self, wallet: Wallet, consensusAlgorithm: ProofOfStake, nodeIdentifier: str = None):
        super().__init__(nodeIdentifier if nodeIdentifier != None else wallet.publicKey)
        self.wallet = wallet
        self.consensusAlgorithm = consensusAlgorithm
        self.blockchain = Blockchain()
        self.__certificateBox = set()
        self.__waitingBlocks = set()

    def new_certificate(self, certificate: Certificate):
        if not isinstance(certificate, Certificate):
            return "Certificate is not a Certificate object"
        if not certificate.is_legit():
            return "Certificate is not legit"
        if self.blockchain.contains_certificate(certificate):
            return "Certificate is already in the blockchain"
        if certificate in self.__certificateBox:
            return "Certificate is already in the certificate box"
        self.__certificateBox.add(certificate)
        if len(self.__certificateBox) >= 5:
            block = Block(self.wallet.publicKey, self.blockchain.get_latest_block().indexInBlockchain + 1, self.blockchain.get_latest_block().hash(), list(self.__certificateBox))
            if self.consensusAlgorithm.is_next_block_forger_legit(self.blockchain.blockList, block):
                self.wallet.sign(block)
                # print(f"Node {self.nodeIdentifier} created a new block")
                self.blockchain.blockList.append(block)
                self.__certificateBox.clear()
                self.broadcast_object(block)
                return "Block added to the blockchain"
            else:
                self.broadcast_object(certificate)
                return "Block forger is not legit"
        else:
            self.broadcast_object(certificate)
        return "Certificate added to the certificate box"

    def new_block(self, block: Block):
        if not isinstance(block, Block):
            return "Block is not a Block object"
        if not block.is_legit():
            return "Block is not legit"
        if self.blockchain.contains_certificate(block):
            return "Block is already in the blockchain"
        if block.indexInBlockchain != self.blockchain.get_latest_block().indexInBlockchain + 1:
            if block.indexInBlockchain > self.blockchain.get_latest_block().indexInBlockchain + 1:
                self.__waitingBlocks.add(block)
                self.broadcast_object(BlockRequest(self.blockchain.get_latest_block().indexInBlockchain + 1))
                return "Sending block request"
            return "Block index is not correct"
        if not self.consensusAlgorithm.is_next_block_forger_legit(self.blockchain.blockList, block):
            return "Block forger is not legit"
        if block.parentBlockHash != self.blockchain.get_latest_block().hash():
            return "Block parent hash is not correct"
        self.blockchain.blockList.append(block)
        self.__certificateBox.update(block.certificateList)
        self.broadcast_object(block)
        # retry to add waiting blocks
        for waitingBlock in self.__waitingBlocks:
            self.new_block(waitingBlock)
        return "Block added to the blockchain"
    
    def clean_certificate_box(self):
        # remove certificates that are already in the blockchain
        self.__certificateBox = {certificate for certificate in self.__certificateBox if not self.blockchain.contains_certificate(certificate)}
    
    def receive_object_from_node(self, obj, nodeIdentifier):
        # debug print
        # print(f"Node {self.nodeIdentifier} received {type(obj)} from node {nodeIdentifier}")
        if isinstance(obj, Block):
            self.new_block(obj)
        elif isinstance(obj, Certificate):
            self.new_certificate(obj)
        elif isinstance(obj, BlockRequest):
            if obj.blockIndex < len(self.blockchain.blockList):
                self.send_object_to_node(self.blockchain.blockList[obj.blockIndex], nodeIdentifier)
        else:
            return "Object is not a Certificate or Block object"
        # print(f"Blockchain: {self.nodeIdentifier}")
        # print(self.blockchain.blockList, len(self.__certificateBox))

class BlockRequest():
    def __init__(self, blockIndex: int):
        self.blockIndex = blockIndex