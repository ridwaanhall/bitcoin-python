"""
Wallet Module for Bitcoin-Python Project
This module implements a simple Bitcoin wallet that can store keys and manage transactions.
"""

import json
import os
from .keygen import KeyGenerator


class Wallet:
    """
    A simple Bitcoin wallet that manages private keys, public keys, and addresses.
    """
    
    def __init__(self, name="default_wallet"):
        """
        Initialize a new wallet.
        
        Args:
            name (str): Name of the wallet
        """
        self.name = name
        self.private_key = None
        self.public_key = None
        self.address = None
        self.balance = 0  # This would be calculated from the blockchain in a real implementation
        
    def generate_new_keypair(self):
        """
        Generate a new keypair for this wallet.
        """
        keypair = KeyGenerator.generate_keypair()
        self.private_key = keypair['private_key']
        self.public_key = keypair['public_key']
        self.address = keypair['address']
        
        print(f"New wallet '{self.name}' created!")
        print(f"Address: {self.address}")
        
    def load_from_private_key(self, private_key_hex):
        """
        Load wallet from an existing private key.
        
        Args:
            private_key_hex (str): Private key in hexadecimal format
        """
        try:
            self.private_key = bytes.fromhex(private_key_hex)
            self.public_key = KeyGenerator.private_key_to_public_key(self.private_key)
            self.address = KeyGenerator.public_key_to_address(self.public_key)
            
            print(f"Wallet '{self.name}' loaded successfully!")
            print(f"Address: {self.address}")
            
        except Exception as e:
            print(f"Error loading wallet: {e}")
            
    def get_private_key_hex(self):
        """
        Get the private key in hexadecimal format.
        
        Returns:
            str: Private key in hex format
        """
        if self.private_key:
            return self.private_key.hex()
        return None
        
    def get_public_key_hex(self):
        """
        Get the public key in hexadecimal format.
        
        Returns:
            str: Public key in hex format
        """
        if self.public_key:
            return self.public_key.hex()
        return None
        
    def get_address(self):
        """
        Get the wallet address.
        
        Returns:
            str: Wallet address
        """
        return self.address
        
    def save_to_file(self, filename=None):
        """
        Save wallet to a JSON file (WARNING: This saves private key in plain text!).
        In a real implementation, the private key should be encrypted.
        
        Args:
            filename (str): Optional filename, defaults to wallet_name.json
        """
        if not filename:
            filename = f"{self.name}.json"
            
        wallet_data = {
            'name': self.name,
            'private_key': self.get_private_key_hex(),
            'public_key': self.get_public_key_hex(),
            'address': self.address,
            'balance': self.balance
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(wallet_data, f, indent=4)
            print(f"Wallet saved to {filename}")
        except Exception as e:
            print(f"Error saving wallet: {e}")
            
    def load_from_file(self, filename):
        """
        Load wallet from a JSON file.
        
        Args:
            filename (str): Path to the wallet file
        """
        try:
            with open(filename, 'r') as f:
                wallet_data = json.load(f)
                
            self.name = wallet_data['name']
            self.private_key = bytes.fromhex(wallet_data['private_key'])
            self.public_key = bytes.fromhex(wallet_data['public_key'])
            self.address = wallet_data['address']
            self.balance = wallet_data.get('balance', 0)
            
            print(f"Wallet loaded from {filename}")
            print(f"Address: {self.address}")
            
        except Exception as e:
            print(f"Error loading wallet from file: {e}")
            
    def display_info(self):
        """
        Display wallet information.
        """
        print(f"\n=== Wallet Info: {self.name} ===")
        print(f"Address: {self.address}")
        print(f"Public Key: {self.get_public_key_hex()}")
        print(f"Balance: {self.balance} BTC")
        print("=" * 40)
        
    def update_balance(self, new_balance):
        """
        Update the wallet balance.
        
        Args:
            new_balance (float): New balance amount
        """
        self.balance = new_balance


def main():
    """
    Demo function to show wallet functionality.
    """
    print("=== Bitcoin Wallet Demo ===")
    
    # Create a new wallet
    wallet = Wallet("demo_wallet")
    wallet.generate_new_keypair()
    
    # Display wallet info
    wallet.display_info()
    
    # Save wallet to file
    wallet.save_to_file()
    
    # Create another wallet and load from the saved file
    wallet2 = Wallet("loaded_wallet")
    wallet2.load_from_file("demo_wallet.json")
    wallet2.display_info()


if __name__ == "__main__":
    main()
