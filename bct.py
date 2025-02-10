import hashlib
import time
import json
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, transactions: List[Dict], previous_hash: str):
        """
        Initialize a new block in the blockchain
        """
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the block using SHA-256
        """
        # Convert block data to string and encode it
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        # Calculate SHA-256 hash
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int):
        """
        Mine the block by finding a hash that starts with the given number of zeros
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty: int = 2):
        """
        Initialize the blockchain with a genesis block
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
        
        # Create genesis block
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block in the chain (genesis block)
        """
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """
        Return the most recent block in the chain
        """
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float):
        """
        Add a new transaction to pending transactions
        """
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self, miner_address: str):
        """
        Create a new block with all pending transactions and mine it
        """
        # Create new block with pending transactions
        block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash
        )
        
        # Mine the block
        block.mine_block(self.difficulty)
        
        # Add block to chain
        self.chain.append(block)
        
        # Clear pending transactions and reward the miner
        self.pending_transactions = [
            {"sender": "network", "recipient": miner_address, "amount": 10.0}
        ]

    def is_chain_valid(self) -> bool:
        """
        Check if the blockchain is valid
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verify current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash in block {i}")
                return False

            # Verify current block links to previous block's hash
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid link between blocks {i-1} and {i}")
                return False

        return True

    def print_blockchain(self):
        """
        Print the contents of the blockchain
        """
        for block in self.chain:
            print("\n=== Block ===")
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")

# Example usage
if __name__ == "__main__":
    # Create blockchain with difficulty 2 (hash must start with "00")
    blockchain = Blockchain(2)
    
    # Add some transactions
    blockchain.add_transaction("Alice", "Bob", 50.0)
    blockchain.add_transaction("Bob", "Charlie", 30.0)
    
    # Mine block with pending transactions
    print("Mining first block...")
    blockchain.mine_pending_transactions("miner1")
    
    # Add more transactions
    blockchain.add_transaction("Charlie", "Alice", 20.0)
    blockchain.add_transaction("Alice", "Bob", 15.0)
    
    # Mine another block
    print("Mining second block...")
    blockchain.mine_pending_transactions("miner1")
    
    # Print the blockchain
    print("\nBlockchain:")
    blockchain.print_blockchain()
    
    # Validate the chain
    print("\nIs blockchain valid?", blockchain.is_chain_valid())
    
    # Demonstrate tampering detection
    print("\nTampering with blockchain...")
    blockchain.chain[1].transactions[0]["amount"] = 100.0
    print("Is blockchain valid after tampering?", blockchain.is_chain_valid())