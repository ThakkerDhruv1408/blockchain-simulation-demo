# Simple Python Blockchain Simulation

## Overview

This project is a simple blockchain simulation implemented in Python, demonstrating core blockchain concepts such as block creation, proof-of-work mining, transaction handling, and chain validation.

## Features

- Block creation with transactions
- Proof-of-work mining mechanism
- Chain validation
- Tamper detection
- Simple transaction management

## Prerequisites

- Python 3.7+
- No external libraries required (uses only standard Python libraries)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/simple-blockchain.git
```

2. Navigate to the project directory:
```bash
cd simple-blockchain
```

## Usage

Run the blockchain simulation:
```bash
python blockchain_simple.py
```

### Simulation Demonstrates:
- Creating a blockchain
- Adding transactions
- Mining blocks
- Validating the blockchain
- Detecting data tampering

## Code Structure

- `Block` class: Represents individual blocks in the chain
- `Blockchain` class: Manages blockchain operations
- `run_blockchain_demo()`: Demonstrates blockchain functionality

## How It Works

1. Creates a genesis block
2. Allows adding transactions
3. Mines blocks with a proof-of-work mechanism
4. Validates chain integrity
5. Detects unauthorized changes

## Learning Objectives

- Understand blockchain fundamental concepts
- Learn basic implementation of blockchain principles
- Explore proof-of-work mechanism
- Understand block validation and tampering detection