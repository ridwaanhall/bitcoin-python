"""
Key Generation Module for Bitcoin-Python Project
This module handles the generation of private keys, public keys, and Bitcoin addresses.
"""

import secrets
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1


class KeyGenerator:
    """
    Handles the generation of cryptographic keys for Bitcoin wallets.
    """
    
    @staticmethod
    def generate_private_key():
        """
        Generate a cryptographically secure random private key.
        
        Returns:
            bytes: 32-byte private key
        """
        # Generate a 256-bit (32-byte) random private key
        return secrets.randbits(256).to_bytes(32, byteorder='big')
    
    @staticmethod
    def private_key_to_public_key(private_key):
        """
        Derive the public key from a private key using ECDSA secp256k1.
        
        Args:
            private_key (bytes): The private key
            
        Returns:
            bytes: The compressed public key (33 bytes)
        """
        # Create signing key from private key
        signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
        # Get the verifying (public) key
        verifying_key = signing_key.verifying_key
        # Return compressed public key format
        return verifying_key.to_string("compressed")
    
    @staticmethod
    def public_key_to_address(public_key):
        """
        Generate a Bitcoin-like address from a public key.
        Process: SHA256 -> RIPEMD160 -> Add version byte -> Checksum -> Base58
        
        Args:
            public_key (bytes): The public key
            
        Returns:
            str: Bitcoin-like address
        """
        # Step 1: SHA256 hash of the public key
        sha256_hash = hashlib.sha256(public_key).digest()
        
        # Step 2: RIPEMD160 hash of the SHA256 hash
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        hash160 = ripemd160.digest()
        
        # Step 3: Add version byte (0x00 for main network)
        version_byte = b'\x00'
        versioned_hash = version_byte + hash160
        
        # Step 4: Calculate checksum (first 4 bytes of double SHA256)
        checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
        
        # Step 5: Concatenate versioned hash and checksum
        full_address = versioned_hash + checksum
        
        # Step 6: Encode in Base58
        address = base58.b58encode(full_address).decode('utf-8')
        
        return address
    
    @staticmethod
    def generate_keypair():
        """
        Generate a complete keypair with address.
        
        Returns:
            dict: Dictionary containing private_key, public_key, and address
        """
        private_key = KeyGenerator.generate_private_key()
        public_key = KeyGenerator.private_key_to_public_key(private_key)
        address = KeyGenerator.public_key_to_address(public_key)
        
        return {
            'private_key': private_key,
            'public_key': public_key,
            'address': address
        }


def main():
    """
    Demo function to show key generation functionality.
    """
    print("=== Bitcoin Key Generation Demo ===")
    
    # Generate a new keypair
    keypair = KeyGenerator.generate_keypair()
    
    print(f"Private Key: {keypair['private_key'].hex()}")
    print(f"Public Key: {keypair['public_key'].hex()}")
    print(f"Address: {keypair['address']}")


if __name__ == "__main__":
    main()
