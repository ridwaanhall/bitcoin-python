"""
Bitcoin-Python Project: A Simple Bitcoin Implementation
Main program that demonstrates the complete Bitcoin simulation.

This program allows users to:
1. Create and manage wallets
2. Create and sign transactions
3. Mine blocks
4. View the blockchain
5. Check balances

Author: Bitcoin-Python Project
Date: 2025
"""

import os
import sys
from wallet.wallet import Wallet
from wallet.keygen import KeyGenerator
from transaction.transaction import Transaction, TransactionPool
from blockchain.chain import Blockchain, BlockchainNode


class BitcoinSimulator:
    """
    Main class that orchestrates the Bitcoin simulation.
    """
    
    def __init__(self):
        """
        Initialize the Bitcoin simulator.
        """
        self.blockchain = Blockchain()
        self.transaction_pool = TransactionPool()
        self.wallets = {}  # Store created wallets
        self.current_wallet = None
        
    def display_menu(self):
        """
        Display the main menu options.
        """
        print("\n" + "="*60)
        print("        BITCOIN-PYTHON SIMULATOR")
        print("="*60)
        print("1. Create New Wallet")
        print("2. Load Existing Wallet")
        print("3. Display Current Wallet Info")
        print("4. Create Transaction")
        print("5. View Transaction Pool")
        print("6. Mine Block")
        print("7. View Blockchain")
        print("8. Check Balance")
        print("9. View Transaction History")
        print("10. Blockchain Statistics")
        print("11. Save Blockchain")
        print("12. Demo Mode (Auto-create wallets and transactions)")
        print("0. Exit")
        print("="*60)
        
    def create_wallet(self):
        """
        Create a new wallet.
        """
        print("\n=== Create New Wallet ===")
        name = input("Enter wallet name: ").strip()
        
        if name in self.wallets:
            print(f"Wallet '{name}' already exists!")
            return
            
        wallet = Wallet(name)
        wallet.generate_new_keypair()
        
        # Save wallet to file
        wallet.save_to_file()
        
        # Store in memory
        self.wallets[name] = wallet
        self.current_wallet = wallet
        
        print(f"Wallet '{name}' created and set as current wallet!")
        
    def load_wallet(self):
        """
        Load an existing wallet from file.
        """
        print("\n=== Load Existing Wallet ===")
        name = input("Enter wallet name: ").strip()
        filename = f"{name}.json"
        
        if not os.path.exists(filename):
            print(f"Wallet file '{filename}' not found!")
            return
            
        wallet = Wallet(name)
        wallet.load_from_file(filename)
        
        # Store in memory
        self.wallets[name] = wallet
        self.current_wallet = wallet
        
        print(f"Wallet '{name}' loaded and set as current wallet!")
        
    def display_wallet_info(self):
        """
        Display current wallet information.
        """
        if not self.current_wallet:
            print("No wallet selected! Please create or load a wallet first.")
            return
            
        self.current_wallet.display_info()
        balance = self.blockchain.get_balance(self.current_wallet.address)
        print(f"Blockchain Balance: {balance} BTC")
        
    def create_transaction(self):
        """
        Create and sign a new transaction.
        """
        if not self.current_wallet:
            print("No wallet selected! Please create or load a wallet first.")
            return
            
        print("\n=== Create Transaction ===")
        print(f"From: {self.current_wallet.address}")
        
        receiver = input("Enter receiver address: ").strip()
        if not receiver:
            print("Receiver address cannot be empty!")
            return
            
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be positive!")
                return
        except ValueError:
            print("Invalid amount!")
            return
            
        # Check if sender has sufficient balance
        current_balance = self.blockchain.get_balance(self.current_wallet.address)
        if current_balance < amount:
            print(f"Insufficient balance! Current balance: {current_balance} BTC")
            return
            
        # Create transaction
        transaction = Transaction(
            self.current_wallet.address,
            receiver,
            amount
        )
        
        # Sign transaction
        transaction.sign_transaction(self.current_wallet.private_key)
        
        # Verify signature
        if transaction.verify_signature(self.current_wallet.public_key):
            self.transaction_pool.add_transaction(transaction)
            transaction.display_info()
        else:
            print("Transaction signature verification failed!")
            
    def view_transaction_pool(self):
        """
        Display all transactions in the pool.
        """
        self.transaction_pool.display_pool()

    def mine_block(self):
        """
        Mine a new block with transactions from the pool.
        """
        print("\n=== Mine Block ===")
        
        transactions = self.transaction_pool.get_transactions()
        if not transactions:
            print("No transactions in pool, mining empty block with coinbase reward only!")
            
        # Ask for mining reward address
        if self.current_wallet:
            miner_address = self.current_wallet.address
            print(f"Mining reward will go to current wallet: {miner_address}")
        else:
            miner_address = input("Enter mining reward address: ").strip()
            if not miner_address:
                print("Mining reward address cannot be empty!")
                return
                
        # Create mining reward transaction
        mining_reward_tx = Transaction(
            "COINBASE",
            miner_address,
            self.blockchain.mining_reward
        )
        
        # Add mining reward to transactions
        all_transactions = transactions + [mining_reward_tx]
        
        # Mine the block
        success = self.blockchain.add_block(all_transactions)
        
        if success:
            # Remove mined transactions from pool
            self.transaction_pool.remove_transactions(transactions)
            print(f"Block mined successfully! Mining reward: {self.blockchain.mining_reward} BTC")
        else:
            print("Mining failed!")
            
    def view_blockchain(self):
        """
        Display the entire blockchain.
        """
        self.blockchain.display_chain()
        
    def check_balance(self):
        """
        Check balance for any address.
        """
        print("\n=== Check Balance ===")
        
        if self.current_wallet:
            default_address = self.current_wallet.address
            if default_address:
                prompt = f"Enter address (press Enter for current wallet: {default_address[:20]}...): "
            else:
                prompt = "Enter address: "
            address = input(prompt).strip()
            if not address:
                address = default_address
        else:
            address = input("Enter address: ").strip()
            
        if not address:
            print("Address cannot be empty!")
            return
            
        balance = self.blockchain.get_balance(address)
        print(f"Balance for {address}: {balance} BTC")
        
    def view_transaction_history(self):
        """
        View transaction history for an address.
        """
        print("\n=== Transaction History ===")
        
        if self.current_wallet:
            default_address = self.current_wallet.address
            address = input(f"Enter address (press Enter for current wallet): ").strip()
            if not address:
                address = default_address
        else:
            address = input("Enter address: ").strip()
            
        if not address:
            print("Address cannot be empty!")
            return
            
        transactions = self.blockchain.get_transaction_history(address)
        
        if not transactions:
            print(f"No transactions found for address: {address}")
            return
            
        print(f"\nTransaction history for {address}:")
        for i, tx in enumerate(transactions, 1):
            tx_type = "Sent" if tx.sender_address == address else "Received"
            print(f"{i}. {tx_type} {tx.amount} BTC - TX ID: {tx.transaction_id[:16]}...")
            
    def blockchain_statistics(self):
        """
        Display blockchain statistics.
        """
        info = self.blockchain.get_blockchain_info()
        print(f"\n=== Blockchain Statistics ===")
        print(f"Total Blocks: {info['total_blocks']}")
        print(f"Total Transactions: {info['total_transactions']}")
        print(f"Total Value Transferred: {info['total_value_transferred']} BTC")
        print(f"Current Difficulty: {info['current_difficulty']}")
        print(f"Mining Reward: {info['mining_reward']} BTC")
        
        # Display all balances
        self.blockchain.display_balances()
        
    def save_blockchain(self):
        """
        Save the blockchain to a file.
        """
        filename = input("Enter filename (default: blockchain.json): ").strip()
        if not filename:
            filename = "blockchain.json"
            
        self.blockchain.save_to_file(filename)
        
    def demo_mode(self):
        """
        Automatically create wallets, transactions, and mine blocks for demonstration.
        """
        print("\n=== Demo Mode ===")
        print("Creating demo wallets and transactions...")
        
        # Create demo wallets
        alice = Wallet("Alice")
        alice.generate_new_keypair()
        
        bob = Wallet("Bob")
        bob.generate_new_keypair()
        
        charlie = Wallet("Charlie")
        charlie.generate_new_keypair()
        
        # Store wallets
        self.wallets["Alice"] = alice
        self.wallets["Bob"] = bob
        self.wallets["Charlie"] = charlie
        self.current_wallet = alice
        
        print("Created wallets for Alice, Bob, and Charlie")
        
        # Give Alice some initial coins (simulate coinbase transaction)
        initial_tx = Transaction("COINBASE", alice.address, 100.0)
        self.blockchain.add_block([initial_tx])
        print("Alice received 100 BTC from coinbase")
        
        # Create some transactions
        tx1 = Transaction(alice.address, bob.address, 25.0)
        tx1.sign_transaction(alice.private_key)
        
        tx2 = Transaction(alice.address, charlie.address, 15.0)
        tx2.sign_transaction(alice.private_key)
        
        self.transaction_pool.add_transaction(tx1)
        self.transaction_pool.add_transaction(tx2)
        
        print("Created transactions: Alice -> Bob (25 BTC), Alice -> Charlie (15 BTC)")
        
        # Mine a block
        mining_reward_tx = Transaction("COINBASE", bob.address, self.blockchain.mining_reward)
        transactions = self.transaction_pool.get_transactions()
        all_transactions = transactions + [mining_reward_tx]
        
        self.blockchain.add_block(all_transactions)
        self.transaction_pool.remove_transactions(transactions)
        
        print("Bob mined a block and received mining reward")
        
        # Create more transactions
        tx3 = Transaction(bob.address, charlie.address, 10.0)
        tx3.sign_transaction(bob.private_key)
        
        tx4 = Transaction(charlie.address, alice.address, 5.0)
        tx4.sign_transaction(charlie.private_key)
        
        self.transaction_pool.add_transaction(tx3)
        self.transaction_pool.add_transaction(tx4)
        
        # Mine another block
        mining_reward_tx2 = Transaction("COINBASE", charlie.address, self.blockchain.mining_reward)
        transactions2 = self.transaction_pool.get_transactions()
        all_transactions2 = transactions2 + [mining_reward_tx2]
        
        self.blockchain.add_block(all_transactions2)
        self.transaction_pool.remove_transactions(transactions2)
        
        print("Charlie mined a block and received mining reward")
        
        print("\nDemo completed! View blockchain and balances to see results.")
        
    def run(self):
        """
        Main program loop.
        """
        print("Welcome to Bitcoin-Python Simulator!")
        print("A simple implementation that represents how Bitcoin works.")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (0-12): ").strip()
                
                if choice == "0":
                    print("Thank you for using Bitcoin-Python Simulator!")
                    break
                elif choice == "1":
                    self.create_wallet()
                elif choice == "2":
                    self.load_wallet()
                elif choice == "3":
                    self.display_wallet_info()
                elif choice == "4":
                    self.create_transaction()
                elif choice == "5":
                    self.view_transaction_pool()
                elif choice == "6":
                    self.mine_block()
                elif choice == "7":
                    self.view_blockchain()
                elif choice == "8":
                    self.check_balance()
                elif choice == "9":
                    self.view_transaction_history()
                elif choice == "10":
                    self.blockchain_statistics()
                elif choice == "11":
                    self.save_blockchain()
                elif choice == "12":
                    self.demo_mode()
                else:
                    print("Invalid choice! Please enter a number between 0-12.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting Bitcoin-Python Simulator...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")


def main():
    """
    Entry point of the program.
    """
    simulator = BitcoinSimulator()
    simulator.run()


if __name__ == "__main__":
    main()
