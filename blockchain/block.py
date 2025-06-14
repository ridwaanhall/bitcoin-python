"""
Block Module for Bitcoin-Python Project
This module implements the Block class that represents a single block in the blockchain.
"""

import hashlib
import json
import time


class Block:
    """
    Represents a single block in the blockchain containing transactions.
    """
    
    def __init__(self, transactions, previous_hash, index=0):
        """
        Initialize a new block.
        
        Args:
            transactions (list): List of Transaction objects
            previous_hash (str): Hash of the previous block
            index (int): Position of this block in the chain
        """
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0  # Used for proof of work
        self.hash = None
        
    def calculate_hash(self):
        """
        Calculate the hash of this block based on its contents.
        
        Returns:
            str: SHA256 hash of the block
        """
        # Create a string representation of the block data
        block_string = (
            str(self.index) +
            str(self.timestamp) +
            str(self.previous_hash) +
            str(self.nonce) +
            self._get_transactions_string()
        )
        
        # Calculate SHA256 hash
        return hashlib.sha256(block_string.encode()).hexdigest()
        
    def _get_transactions_string(self):
        """
        Create a string representation of all transactions in the block.
        
        Returns:
            str: Concatenated transaction data
        """
        transactions_string = ""
        for transaction in self.transactions:
            transactions_string += transaction.transaction_id
        return transactions_string
        
    def mine_block(self, difficulty=4):
        """
        Mine the block using proof of work algorithm.
        Find a nonce that makes the block hash start with a certain number of zeros.
        
        Args:
            difficulty (int): Number of leading zeros required in the hash
        """
        target = "0" * difficulty
        
        print(f"Mining block {self.index}...")
        start_time = time.time()
        
        while True:
            # Calculate hash with current nonce
            self.hash = self.calculate_hash()
            
            # Check if hash meets difficulty requirement
            if self.hash[:difficulty] == target:
                end_time = time.time()
                mining_time = end_time - start_time
                print(f"Block {self.index} mined successfully!")
                print(f"Hash: {self.hash}")
                print(f"Nonce: {self.nonce}")
                print(f"Mining time: {mining_time:.2f} seconds")
                break
                
            # Increment nonce and try again
            self.nonce += 1
            
    def is_valid(self, previous_block=None):
        """
        Validate the block.
        
        Args:
            previous_block (Block): The previous block in the chain
            
        Returns:
            bool: True if block is valid, False otherwise
        """
        # Check if block has been mined (hash exists)
        if not self.hash:
            print(f"Block {self.index} has not been mined!")
            return False
            
        # Verify that the hash is correct
        if self.hash != self.calculate_hash():
            print(f"Block {self.index} hash is invalid!")
            return False
            
        # If not genesis block, check previous hash
        if previous_block:
            if self.previous_hash != previous_block.hash:
                print(f"Block {self.index} previous hash is invalid!")
                return False
                
        # Validate all transactions in the block
        for transaction in self.transactions:
            if not transaction.is_valid():
                print(f"Block {self.index} contains invalid transaction!")
                return False
                
        return True
        
    def get_total_amount(self):
        """
        Calculate the total amount of all transactions in this block.
        
        Returns:
            float: Total transaction amount
        """
        return sum(transaction.amount for transaction in self.transactions)
        
    def to_dict(self):
        """
        Convert block to dictionary format.
        
        Returns:
            dict: Block data as dictionary
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'nonce': self.nonce,
            'transactions': [tx.to_dict() for tx in self.transactions]
        }
        
    def to_json(self):
        """
        Convert block to JSON string.
        
        Returns:
            str: Block data as JSON string
        """
        return json.dumps(self.to_dict(), indent=2)
        
    def display_info(self):
        """
        Display block information in a readable format.
        """
        print(f"\n=== Block {self.index} ===")
        print(f"Timestamp: {time.ctime(self.timestamp)}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Hash: {self.hash}")
        print(f"Nonce: {self.nonce}")
        print(f"Transactions: {len(self.transactions)}")
        print(f"Total Amount: {self.get_total_amount()} BTC")
        
        if self.transactions:
            print("\nTransactions in this block:")
            for i, tx in enumerate(self.transactions, 1):
                print(f"  {i}. {tx.transaction_id[:8]}... | {tx.amount} BTC | {tx.sender_address[:8]}... -> {tx.receiver_address[:8]}...")
                
        print("=" * 50)


def create_genesis_block():
    """
    Create the first block in the blockchain (Genesis Block).
    
    Returns:
        Block: The genesis block
    """
    # Genesis block has no transactions and previous hash is "0"
    genesis_block = Block([], "0", 0)
    genesis_block.mine_block(difficulty=2)  # Easier difficulty for genesis block
    return genesis_block


def main():
    """
    Demo function to show block functionality.
    """
    print("=== Bitcoin Block Demo ===")
    
    # Create genesis block
    genesis = create_genesis_block()
    genesis.display_info()
    
    # Create a mock transaction for testing
    from transaction.transaction import Transaction
    
    mock_transaction = Transaction(
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
        1.5
    )
    
    # Create a new block with the transaction
    new_block = Block([mock_transaction], genesis.hash, 1)
    new_block.mine_block(difficulty=3)
    new_block.display_info()


if __name__ == "__main__":
    main()
