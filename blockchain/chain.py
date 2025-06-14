"""
Blockchain Module for Bitcoin-Python Project
This module implements the main Blockchain class that manages the chain of blocks.
"""

import json
import time
from .block import Block, create_genesis_block


class Blockchain:
    """
    Represents the complete blockchain containing all blocks and providing
    functionality to add new blocks, validate the chain, and manage balances.
    """
    
    def __init__(self):
        """
        Initialize a new blockchain with the genesis block.
        """
        self.chain = [create_genesis_block()]
        self.difficulty = 4  # Mining difficulty (number of leading zeros)
        self.mining_reward = 10.0  # Reward for mining a block
        self.balances = {}  # Track account balances
        
    def get_latest_block(self):
        """
        Get the most recent block in the chain.
        
        Returns:
            Block: The latest block
        """
        return self.chain[-1]
        
    def add_block(self, transactions):
        """
        Add a new block to the blockchain with the given transactions.
        
        Args:
            transactions (list): List of Transaction objects
        """
        if not transactions:
            print("Cannot create block with no transactions!")
            return False
            
        # Create new block
        previous_block = self.get_latest_block()
        new_block = Block(
            transactions,
            previous_block.hash,
            len(self.chain)
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Validate the block before adding
        if new_block.is_valid(previous_block):
            self.chain.append(new_block)
            self._update_balances(transactions)
            print(f"Block {new_block.index} added to blockchain!")
            return True
        else:
            print("Block validation failed!")
            return False
    
    def _update_balances(self, transactions):
        """
        Update account balances based on transactions.
        
        Args:
            transactions (list): List of Transaction objects
        """
        for transaction in transactions:
            # Handle coinbase transactions (mining rewards) - don't deduct from sender
            if transaction.sender_address == "COINBASE":
                # Only add to receiver (new coins created)
                if transaction.receiver_address in self.balances:
                    self.balances[transaction.receiver_address] += transaction.amount
                else:
                    self.balances[transaction.receiver_address] = transaction.amount
            else:
                # Regular transactions - deduct from sender, add to receiver
                if transaction.sender_address in self.balances:
                    self.balances[transaction.sender_address] -= transaction.amount
                else:
                    self.balances[transaction.sender_address] = -transaction.amount
                    
                # Add to receiver
                if transaction.receiver_address in self.balances:
                    self.balances[transaction.receiver_address] += transaction.amount
                else:
                    self.balances[transaction.receiver_address] = transaction.amount
                
    def get_balance(self, address):
        """
        Get the balance for a specific address.
        
        Args:
            address (str): The address to check
            
        Returns:
            float: Current balance
        """
        return self.balances.get(address, 0.0)
        
    def is_chain_valid(self):
        """
        Validate the entire blockchain.
        
        Returns:
            bool: True if blockchain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Validate current block
            if not current_block.is_valid(previous_block):
                return False
                
        return True
        
    def get_transaction_history(self, address):
        """
        Get all transactions involving a specific address.
        
        Args:
            address (str): The address to search for
            
        Returns:
            list: List of transactions involving the address
        """
        transactions = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if (transaction.sender_address == address or 
                    transaction.receiver_address == address):
                    transactions.append(transaction)
                    
        return transactions
        
    def find_transaction(self, transaction_id):
        """
        Find a transaction by its ID.
        
        Args:
            transaction_id (str): The transaction ID to search for
            
        Returns:
            Transaction or None: The transaction if found, None otherwise
        """
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.transaction_id == transaction_id:
                    return transaction
        return None
        
    def get_blockchain_info(self):
        """
        Get general information about the blockchain.
        
        Returns:
            dict: Blockchain statistics
        """
        total_transactions = sum(len(block.transactions) for block in self.chain)
        total_value = sum(block.get_total_amount() for block in self.chain)
        
        return {
            'total_blocks': len(self.chain),
            'total_transactions': total_transactions,
            'total_value_transferred': total_value,
            'current_difficulty': self.difficulty,
            'mining_reward': self.mining_reward
        }
        
    def to_dict(self):
        """
        Convert blockchain to dictionary format.
        
        Returns:
            dict: Blockchain data as dictionary
        """
        return {
            'chain': [block.to_dict() for block in self.chain],
            'difficulty': self.difficulty,
            'mining_reward': self.mining_reward,
            'balances': self.balances
        }
        
    def save_to_file(self, filename="blockchain.json"):
        """
        Save the blockchain to a JSON file.
        
        Args:
            filename (str): Name of the file to save to
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            print(f"Blockchain saved to {filename}")
        except Exception as e:
            print(f"Error saving blockchain: {e}")
            
    def display_chain(self):
        """
        Display the entire blockchain in a readable format.
        """
        print(f"\n=== Blockchain ({len(self.chain)} blocks) ===")
        
        for block in self.chain:
            block.display_info()
            
        # Display blockchain statistics
        info = self.get_blockchain_info()
        print(f"\n=== Blockchain Statistics ===")
        print(f"Total Blocks: {info['total_blocks']}")
        print(f"Total Transactions: {info['total_transactions']}")
        print(f"Total Value Transferred: {info['total_value_transferred']} BTC")
        print(f"Current Difficulty: {info['current_difficulty']}")
        print(f"Mining Reward: {info['mining_reward']} BTC")
        print("=" * 50)
        
    def display_balances(self):
        """
        Display all account balances.
        """
        print(f"\n=== Account Balances ===")
        if not self.balances:
            print("No accounts with balances")
        else:
            for address, balance in self.balances.items():
                print(f"{address}: {balance} BTC")
        print("=" * 40)


class BlockchainNode:
    """
    Represents a node in the Bitcoin network that maintains a blockchain.
    """
    
    def __init__(self, node_id):
        """
        Initialize a blockchain node.
        
        Args:
            node_id (str): Unique identifier for this node
        """
        self.node_id = node_id
        self.blockchain = Blockchain()
        self.mempool = []  # Pending transactions
        
    def add_transaction_to_mempool(self, transaction):
        """
        Add a transaction to the memory pool.
        
        Args:
            transaction (Transaction): Transaction to add
        """
        if transaction.is_valid():
            self.mempool.append(transaction)
            print(f"Transaction added to mempool by node {self.node_id}")
        else:
            print("Invalid transaction rejected by node")
            
    def mine_pending_transactions(self, mining_reward_address):
        """
        Mine all pending transactions and add them to the blockchain.
        
        Args:
            mining_reward_address (str): Address to receive mining reward
        """
        if not self.mempool:
            print("No transactions to mine!")
            return
            
        # Create mining reward transaction
        from transaction.transaction import Transaction
        reward_tx = Transaction("COINBASE", mining_reward_address, self.blockchain.mining_reward)
        
        # Add mining reward to transactions
        transactions_to_mine = self.mempool.copy()
        transactions_to_mine.append(reward_tx)
        
        # Mine the block
        success = self.blockchain.add_block(transactions_to_mine)
        
        if success:
            # Clear mempool after successful mining
            self.mempool.clear()
            print(f"Mining completed by node {self.node_id}!")
        else:
            print("Mining failed!")


def main():
    """
    Demo function to show blockchain functionality.
    """
    print("=== Bitcoin Blockchain Demo ===")
    
    # Create a blockchain
    blockchain = Blockchain()
    
    # Create some mock transactions
    from transaction.transaction import Transaction
    
    tx1 = Transaction("Alice", "Bob", 5.0)
    tx2 = Transaction("Bob", "Charlie", 2.0)
    tx3 = Transaction("Charlie", "Alice", 1.0)
    
    # Add blocks with transactions
    blockchain.add_block([tx1])
    blockchain.add_block([tx2, tx3])
    
    # Display the blockchain
    blockchain.display_chain()
    blockchain.display_balances()
    
    # Validate the blockchain
    is_valid = blockchain.is_chain_valid()
    print(f"\nBlockchain is valid: {is_valid}")


if __name__ == "__main__":
    main()
