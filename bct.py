import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Calculate block hash including nonce
        block_data = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Find a hash starting with '0' * difficulty
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} mined! Hash: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2  # Number of leading zeros required in hash
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_transaction(self, sender, receiver, amount):
        # Add a new transaction to pending transactions
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

    def mine_pending_transactions(self, miner_reward_address):
        # Create a new block with pending transactions
        block = Block(len(self.chain), self.pending_transactions, self.chain[-1].hash)
        block.mine_block(self.difficulty)
        
        # Add block to chain
        self.chain.append(block)
        
        # Reset pending transactions and reward miner
        self.pending_transactions = [
            {'sender': 'network', 'receiver': miner_reward_address, 'amount': 10}
        ]

    def is_chain_valid(self):
        # Check if the blockchain is valid
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Check current block's hash
            if current.hash != current.calculate_hash():
                return False

            # Check link to previous block
            if current.previous_hash != previous.hash:
                return False

        return True

    def print_chain(self):
        # Print all blocks in the chain
        for block in self.chain:
            print("\n====================")
            print(f"Block #{block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print("Transactions:")
            for tx in block.transactions:
                print(f"  {tx['sender']} -> {tx['receiver']}: {tx['amount']}")

# Demo simulation
def run_blockchain_demo():
    # Create blockchain
    print("Creating blockchain...")
    coin = Blockchain()

    # Add some transactions
    print("\nAdding transactions...")
    coin.add_transaction("Alice", "Bob", 50)
    coin.add_transaction("Bob", "Charlie", 30)
    
    # Mine first block
    print("\nMining first block...")
    coin.mine_pending_transactions("miner1")

    # Add more transactions
    print("\nAdding more transactions...")
    coin.add_transaction("Charlie", "David", 20)
    coin.add_transaction("David", "Alice", 15)
    
    # Mine second block
    print("\nMining second block...")
    coin.mine_pending_transactions("miner1")

    # Print the blockchain
    print("\nBLOCKCHAIN:")
    coin.print_chain()

    # Validate chain
    print("\nIs blockchain valid?", coin.is_chain_valid())

    # Demonstrate tampering detection
    print("\nTampering with blockchain...")
    coin.chain[1].transactions[0]['amount'] = 100
    print("Is blockchain still valid?", coin.is_chain_valid())

if __name__ == "__main__":
    run_blockchain_demo()