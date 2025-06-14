"""
Transaction Module for Bitcoin-Python Project
This module handles the creation, signing, and verification of transactions.
"""

import hashlib
import json
import time
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError


class Transaction:
    """
    Represents a Bitcoin-like transaction with digital signature capabilities.
    """
    
    def __init__(self, sender_address, receiver_address, amount, timestamp=None):
        """
        Initialize a new transaction.
        
        Args:
            sender_address (str): Address of the sender
            receiver_address (str): Address of the receiver
            amount (float): Amount to transfer
            timestamp (float): Optional timestamp, defaults to current time
        """
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount
        self.timestamp = timestamp if timestamp else time.time()
        self.signature = None
        self.transaction_id = self._calculate_transaction_id()
        
    def _calculate_transaction_id(self):
        """
        Calculate a unique transaction ID based on transaction data.
        
        Returns:
            str: Transaction ID (SHA256 hash)
        """
        # Create a string representation of the transaction data
        transaction_string = f"{self.sender_address}{self.receiver_address}{self.amount}{self.timestamp}"
        
        # Calculate SHA256 hash
        return hashlib.sha256(transaction_string.encode()).hexdigest()
        
    def get_transaction_data_for_signing(self):
        """
        Get the transaction data that needs to be signed.
        
        Returns:
            str: Transaction data string for signing
        """
        return f"{self.sender_address}{self.receiver_address}{self.amount}{self.timestamp}"
        
    def sign_transaction(self, private_key):
        """
        Sign the transaction using the sender's private key.
        
        Args:
            private_key (bytes): Private key of the sender
        """
        try:
            # Create signing key from private key
            signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
            
            # Get the data to be signed
            data_to_sign = self.get_transaction_data_for_signing().encode()
            
            # Sign the data
            self.signature = signing_key.sign(data_to_sign)
            
            print(f"Transaction {self.transaction_id[:8]}... signed successfully!")
            
        except Exception as e:
            print(f"Error signing transaction: {e}")
            
    def verify_signature(self, public_key):
        """
        Verify the transaction signature using the sender's public key.
        
        Args:
            public_key (bytes): Public key of the sender
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not self.signature:
            print("Transaction is not signed!")
            return False
            
        try:
            # Create verifying key from public key
            verifying_key = VerifyingKey.from_string(public_key, curve=SECP256k1)
            
            # Get the original data that was signed
            data_to_verify = self.get_transaction_data_for_signing().encode()
            
            # Verify the signature
            verifying_key.verify(self.signature, data_to_verify)
            return True
            
        except BadSignatureError:
            print("Invalid signature!")
            return False
        except Exception as e:
            print(f"Error verifying signature: {e}")
            return False
            
    def is_valid(self):
        """
        Check if the transaction is valid (basic validation).
        
        Returns:
            bool: True if transaction is valid, False otherwise
        """
        # Check if amount is positive
        if self.amount <= 0:
            print("Transaction amount must be positive!")
            return False
              # Check if sender and receiver are different (except for coinbase transactions)
        if self.sender_address == self.receiver_address and self.sender_address != "COINBASE":
            print("Sender and receiver cannot be the same!")
            return False
            
        # Check if transaction is signed (coinbase transactions don't need signatures)
        if not self.signature and self.sender_address != "COINBASE":
            print("Transaction must be signed!")
            return False
            
        return True
        
    def to_dict(self):
        """
        Convert transaction to dictionary format.
        
        Returns:
            dict: Transaction data as dictionary
        """
        return {
            'transaction_id': self.transaction_id,
            'sender_address': self.sender_address,
            'receiver_address': self.receiver_address,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature.hex() if self.signature else None
        }
        
    def to_json(self):
        """
        Convert transaction to JSON string.
        
        Returns:
            str: Transaction data as JSON string
        """
        return json.dumps(self.to_dict(), indent=2)
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a Transaction object from dictionary data.
        
        Args:
            data (dict): Transaction data dictionary
            
        Returns:
            Transaction: Transaction object
        """
        transaction = cls(
            data['sender_address'],
            data['receiver_address'],
            data['amount'],
            data['timestamp']
        )
        
        if data.get('signature'):
            transaction.signature = bytes.fromhex(data['signature'])
            
        return transaction
        
    def display_info(self):
        """
        Display transaction information in a readable format.
        """
        print(f"\n=== Transaction {self.transaction_id[:8]}... ===")
        print(f"From: {self.sender_address}")
        print(f"To: {self.receiver_address}")
        print(f"Amount: {self.amount} BTC")
        print(f"Timestamp: {time.ctime(self.timestamp)}")
        print(f"Signed: {'Yes' if self.signature else 'No'}")
        print("=" * 50)


class TransactionPool:
    """
    A simple transaction pool (mempool) to store unconfirmed transactions.
    """
    
    def __init__(self):
        """
        Initialize an empty transaction pool.
        """
        self.transactions = []
        
    def add_transaction(self, transaction):
        """
        Add a transaction to the pool.
        
        Args:
            transaction (Transaction): Transaction to add
        """
        if transaction.is_valid():
            self.transactions.append(transaction)
            print(f"Transaction {transaction.transaction_id[:8]}... added to pool")
        else:
            print("Invalid transaction, not added to pool")
            
    def get_transactions(self, max_count=None):
        """
        Get transactions from the pool.
        
        Args:
            max_count (int): Maximum number of transactions to return
            
        Returns:
            list: List of transactions
        """
        if max_count:
            return self.transactions[:max_count]
        return self.transactions.copy()
        
    def remove_transactions(self, transactions):
        """
        Remove transactions from the pool (after they're included in a block).
        
        Args:
            transactions (list): List of transactions to remove
        """
        for transaction in transactions:
            if transaction in self.transactions:
                self.transactions.remove(transaction)
                
    def clear_pool(self):
        """
        Clear all transactions from the pool.
        """
        self.transactions.clear()
        print("Transaction pool cleared")
        
    def display_pool(self):
        """
        Display all transactions in the pool.
        """
        print(f"\n=== Transaction Pool ({len(self.transactions)} transactions) ===")
        if not self.transactions:
            print("Pool is empty")
        else:
            for i, tx in enumerate(self.transactions, 1):
                print(f"{i}. {tx.transaction_id[:8]}... | {tx.amount} BTC | {tx.sender_address[:8]}... -> {tx.receiver_address[:8]}...")
        print("=" * 60)


def main():
    """
    Demo function to show transaction functionality.
    """
    print("=== Bitcoin Transaction Demo ===")
    
    # Mock wallet data for demo
    sender_private_key = bytes.fromhex("1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
    sender_public_key = bytes.fromhex("02" + "1234567890abcdef" * 4)  # Mock public key
    sender_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    receiver_address = "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"
    
    # Create a transaction
    transaction = Transaction(sender_address, receiver_address, 0.5)
    transaction.display_info()
    
    # Sign the transaction
    transaction.sign_transaction(sender_private_key)
    
    # Verify the signature
    is_valid = transaction.verify_signature(sender_public_key)
    print(f"Signature valid: {is_valid}")
    
    # Create a transaction pool
    pool = TransactionPool()
    pool.add_transaction(transaction)
    pool.display_pool()


if __name__ == "__main__":
    main()
