import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + previous_hash + str(timestamp) + data
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

def print_blockchain(blockchain):
    for block in blockchain:
        print(f"Block #{block.index}:")
        print(f"  Previous Block's Hash (like a fingerprint): {block.previous_hash}")
        print(f"  Current Block's Hash (its own fingerprint): {block.hash}")
        print(f"  Information in the Block: {block.data}")
        print(f"  Time when it was added: {time.ctime(block.timestamp)}")
        print("-" * 30)

def is_chain_valid(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]
        if current_block.previous_hash != previous_block.hash:
            print(f"Block #{current_block.index} has been tampered with!")
            return False
        if current_block.hash != calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
            print(f"Block #{current_block.index} has invalid hash!")
            return False
    return True

# Initialize blockchain
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Add new blocks with student grades
grades = [
    {"name": "Alice", "subject": "Math", "grade": "A"},
    {"name": "Bob", "subject": "Science", "grade": "B"},
    {"name": "Charlie", "subject": "History", "grade": "C"}
]

for grade in grades:
    new_block_data = f"Student: {grade['name']}, Subject: {grade['subject']}, Grade: {grade['grade']}"
    new_block = create_new_block(previous_block, new_block_data)
    blockchain.append(new_block)
    previous_block = new_block

# Print the original blockchain
print("Original Blockchain:")
print_blockchain(blockchain)

# Check if the blockchain is valid
print("Is the original blockchain valid?", is_chain_valid(blockchain))

# Tamper with the blockchain
blockchain[2].data = "Tampered Data"
blockchain[2].hash = calculate_hash(blockchain[2].index, blockchain[2].previous_hash, blockchain[2].timestamp, blockchain[2].data)

# Print the tampered blockchain
print("Tampered Blockchain:")
print_blockchain(blockchain)

# Check if the blockchain is valid after tampering
print("Is the tampered blockchain valid?", is_chain_valid(blockchain))
