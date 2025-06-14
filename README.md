# Bitcoin-Python Project: A Simple Bitcoin Implementation

A complete, educational implementation of Bitcoin's core concepts in Python. This project demonstrates how Bitcoin works conceptually while remaining simple and clear for learning purposes.

## 🎯 Project Overview

This project implements the fundamental components of Bitcoin:

- **Wallet Creation**: Generate private keys, public keys, and Bitcoin-like addresses
- **Transaction System**: Create, sign, and verify transactions using ECDSA
- **Blockchain**: Implement blocks with proof-of-work mining
- **Transaction Pool**: Manage pending transactions (mempool)
- **Balance Management**: Track account balances across the blockchain

## 📁 Project Structure

```txt
bitcoin-python/
├── wallet/
│   ├── __init__.py
│   ├── keygen.py          # Key generation (private key, public key, address)
│   └── wallet.py          # Wallet management and storage
├── transaction/
│   ├── __init__.py
│   └── transaction.py     # Transaction creation, signing, and verification
├── blockchain/
│   ├── __init__.py
│   ├── block.py          # Block structure and mining
│   └── chain.py          # Blockchain management and validation
├── main.py               # Main program with interactive menu
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Installation and Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/ridwaanhall/bitcoin-python.git
cd bitcoin-python
```

### Step 2: Create Virtual Environment (Recommended)

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Or if you're using Command Prompt
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Run the Project

```powershell
python main.py
```

## 🎮 How to Use

### Quick Start with Demo Mode

1. Run the program: `python main.py`
2. Choose option `12` (Demo Mode) to automatically create wallets and transactions
3. Explore the blockchain with options `7` (View Blockchain) and `10` (Statistics)

### Manual Step-by-Step Usage

#### 1. Create Your First Wallet

- Choose option `1` (Create New Wallet)
- Enter a wallet name (e.g., "MyWallet")
- Your private key, public key, and address will be generated automatically
- The wallet is saved to a JSON file

#### 2. Create a Transaction

- Choose option `4` (Create Transaction)
- Enter the receiver's address
- Enter the amount to send
- The transaction will be signed and added to the transaction pool

#### 3. Mine a Block

- Choose option `6` (Mine Block)
- The program will mine all pending transactions into a new block
- Mining uses proof-of-work (finding a hash with leading zeros)
- The miner receives a reward (default: 10 BTC)

#### 4. View Results

- Option `7`: View the entire blockchain
- Option `8`: Check balance for any address
- Option `9`: View transaction history for an address
- Option `10`: Display blockchain statistics

## 🔧 Key Components Explained

### 1. Wallet System (`wallet/`)

**Key Generation (`keygen.py`)**:

- Generates cryptographically secure 256-bit private keys
- Derives public keys using ECDSA secp256k1 curve
- Creates Bitcoin-like addresses using SHA256 + RIPEMD160 + Base58 encoding

**Wallet Management (`wallet.py`)**:

- Stores private keys, public keys, and addresses
- Saves/loads wallets to/from JSON files
- Manages wallet balance tracking

### 2. Transaction System (`transaction/`)

**Transaction Class**:

- Contains sender address, receiver address, amount, and timestamp
- Supports digital signatures using ECDSA
- Includes signature verification methods
- Maintains a transaction pool (mempool) for pending transactions

**Key Features**:

- Transaction validation (positive amounts, different sender/receiver)
- Digital signature creation and verification
- Transaction ID generation using SHA256
- JSON serialization for storage

### 3. Blockchain System (`blockchain/`)

**Block Structure (`block.py`)**:

- Contains index, timestamp, transactions, previous hash, nonce, and current hash
- Implements proof-of-work mining algorithm
- Validates block integrity and transaction validity

**Blockchain Management (`chain.py`)**:

- Maintains the chain of blocks starting with a genesis block
- Validates the entire blockchain integrity
- Manages account balances across all transactions
- Provides transaction history and search functionality

### 4. Proof-of-Work Mining

The mining process:

1. Takes pending transactions from the pool
2. Creates a new block with these transactions
3. Finds a nonce that makes the block hash start with leading zeros
4. The difficulty determines how many leading zeros are required
5. Miners receive a reward for successfully mining a block

## 🔒 Cryptographic Implementation

### ECDSA (Elliptic Curve Digital Signature Algorithm)

- Uses secp256k1 curve (same as Bitcoin)
- Private key: 256-bit random number
- Public key: Derived from private key using elliptic curve multiplication
- Signatures: Prove ownership without revealing the private key

### Hashing Functions

- **SHA256**: Used for transaction IDs, block hashes, and address generation
- **RIPEMD160**: Used in address generation for shorter hash
- **Base58**: Encoding for Bitcoin-like addresses (avoids confusing characters)

## 🎓 Educational Value

This project demonstrates:

1. **Cryptographic Concepts**: Public-key cryptography, digital signatures, hash functions
2. **Blockchain Structure**: Linked blocks, merkle-like transaction organization
3. **Consensus Mechanism**: Proof-of-work mining and difficulty adjustment
4. **Network Economics**: Mining rewards, transaction fees, balance management
5. **Data Integrity**: Chain validation, transaction verification

## 🛠️ Technical Features

### Security Features

- Cryptographically secure random number generation
- ECDSA signature verification
- Block hash validation
- Chain integrity checking

### Performance Considerations

- Adjustable mining difficulty
- Transaction batching in blocks
- Efficient balance calculation
- Memory-based transaction pool

### Extensibility

- Modular design allows easy feature addition
- Clear separation of concerns
- JSON serialization for data persistence
- Comprehensive error handling

## 🔍 Example Usage Scenarios

### Scenario 1: Basic Wallet Operations

```txt
1. Create wallet "Alice"
2. Create wallet "Bob"
3. View Alice's wallet info
4. Create transaction: Alice -> Bob (10 BTC)
5. Mine block
6. Check balances
```

### Scenario 2: Multi-User Transaction Chain

```txt
1. Run Demo Mode (creates Alice, Bob, Charlie with transactions)
2. View blockchain to see transaction history
3. Check individual balances
4. Create additional transactions
5. Mine new blocks
```

### Scenario 3: Blockchain Validation

```txt
1. Create several transactions and blocks
2. View blockchain statistics
3. Save blockchain to file
4. Restart program and verify integrity
```

## 🚧 Limitations and Simplifications

This is an educational implementation with several simplifications:

1. **Network**: No peer-to-peer networking (single node)
2. **Persistence**: Limited file-based storage (no database)
3. **Security**: Private keys stored in plain text
4. **Scalability**: In-memory operations only
5. **Consensus**: Simple proof-of-work (no difficulty adjustment)
6. **Transaction Types**: Only basic transfers (no scripts)

## 🔮 Potential Extensions

### Network Module (Advanced)

- Implement peer-to-peer communication using sockets
- Add node discovery and blockchain synchronization
- Implement consensus rules for multiple nodes

### Enhanced Security

- Encrypt private key storage
- Add multi-signature transactions
- Implement HD (Hierarchical Deterministic) wallets

### Additional Features

- Transaction fees
- Script-based transactions
- Merkle tree implementation for transaction verification
- RESTful API for external access

## 📚 Learning Resources

To better understand the concepts implemented:

1. **Bitcoin Whitepaper**: Original Bitcoin paper by Satoshi Nakamoto
2. **Mastering Bitcoin**: Comprehensive guide to Bitcoin technology
3. **Cryptography**: Study elliptic curve cryptography and digital signatures
4. **Blockchain Technology**: Understanding distributed ledgers and consensus

## 🤝 Contributing

This is an educational project. Suggestions for improvements:

- Better error handling
- More comprehensive tests
- Additional transaction types
- Performance optimizations
- Better user interface

## 📄 License

This project is created for educational purposes. Feel free to use, modify, and distribute for learning.

## ⚠️ Disclaimer

This is a simplified educational implementation. Do NOT use this code for any real cryptocurrency or financial applications. Real Bitcoin implementations require much more sophisticated security, networking, and consensus mechanisms.
