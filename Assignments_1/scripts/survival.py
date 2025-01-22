import random
from typing import List, Self, Tuple

class Node:
    name: str
    neighbors: List[Self]
    message: List[str]

    def __init__(self, _name) -> None:
        self.name = _name
        self.message = [""] * 5

    def reboot(self, connectedNodes: List[Self]):
        self.neighbors = connectedNodes
        self.message = ["", "", "", "" ,""]

    def tell_message(self):
        output = f"[{self.name}]"
        for w in self.message:
            if not w:
                output += " ???"
            else:
                output += f" {w}"
        return output

    def deliver_message_bit(self, index:int, messageBit: str):
        if index < 1 or index > 5:
            return
        
        self.message[index- 1] = messageBit

    def send_random_message_bit_to_neighbors(self):
        # Choose a random index of a non empty message
        validIndexs = [i for i in range(5) if self.message[i]]
        if not validIndexs:
            return
        index = random.choice(validIndexs)

        for node in self.neighbors:
            node.message[index] = self.message[index]

class Simulation:
    nodeCount: int
    nodes: List[Node]
    connectProbability: float
    crashProbability: float

    def __init__(self, _nodeCount: int, _connectProbability: float, _crashProbability: float) -> None:
        self.nodeCount = _nodeCount
        self.connectProbability = _connectProbability
        self.crashProbability = _crashProbability
        self.nodes = [Node(f'Node {i+1}') for i in range(self.nodeCount)]
        for node in self.nodes:
            node.message = ["taking", "the","hobbit", "to", "isengard"]
            node.neighbors = [n for n in self.nodes if n != node]


    def reboot_node_with_random_neighbors(self, nodeToReboot: Node, potentialNeighbors: List[Node]):
        # print("potentialNeighbors",potentialNeighbors)
        neighbors = [node for node in potentialNeighbors if random.random() < self.connectProbability]
        # print("neighbors",neighbors)
        nodeToReboot.reboot(neighbors)
    
    def run(self, days: int):
        for i in range(days):
            for node in self.nodes:
                if random.random() < self.crashProbability:
                    self.reboot_node_with_random_neighbors(node, [n for n in self.nodes if n != node])
                else:
                    node.send_random_message_bit_to_neighbors()
            isMessageLost = True
            for node in self.nodes:
                if node.message == ["taking", "the","hobbit", "to", "isengard"]:
                    isMessageLost = False
                    break
            if isMessageLost:
                print(f"Day {i+1}: Message lost")
                break
        for node in self.nodes:
            print(node.tell_message())
