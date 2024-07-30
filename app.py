from flask import Flask, jsonify, request, render_template
import hashlib
import time

app = Flask(__name__)

class Block:
    def __init__(self, index, previous_hash, timestamp, sender, receiver, amount, hash, is_tampered=False):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.hash = hash
        self.is_tampered = is_tampered  # Flag to indicate tampering

def calculate_hash(index, previous_hash, timestamp, sender, receiver, amount):
    value = str(index) + previous_hash + str(timestamp) + sender + receiver + str(amount)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "genesis", "genesis", 0, calculate_hash(0, "0", int(time.time()), "genesis", "genesis", 0))

def create_new_block(previous_block, sender, receiver, amount):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, sender, receiver, amount)
    return Block(index, previous_block.hash, timestamp, sender, receiver, amount, hash)

def recalculate_hashes():
    tampered_blocks = []
    for i in range(len(blockchain)):
        if i == 0:
            blockchain[i].hash = calculate_hash(blockchain[i].index, blockchain[i].previous_hash, blockchain[i].timestamp, blockchain[i].sender, blockchain[i].receiver, blockchain[i].amount)
        else:
            new_hash = calculate_hash(blockchain[i].index, blockchain[i].previous_hash, blockchain[i].timestamp, blockchain[i].sender, blockchain[i].receiver, blockchain[i].amount)
            if blockchain[i].hash != new_hash:
                blockchain[i].is_tampered = True
                tampered_blocks.append(blockchain[i].index)
                blockchain[i].hash = new_hash  # Recalculate correct hash

    if tampered_blocks:
        print(f"Chain is broken! Tampered blocks at indices: {tampered_blocks}")

# Initialize blockchain
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain = []
    for block in blockchain:
        chain.append({
            'index': block.index,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'sender': block.sender,
            'receiver': block.receiver,
            'amount': block.amount,
            'hash': block.hash,
            'is_tampered': block.is_tampered
        })
    return jsonify(chain)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    global previous_block
    sender = request.json.get('sender', '')
    receiver = request.json.get('receiver', '')
    amount = request.json.get('amount', 0)
    new_block = create_new_block(previous_block, sender, receiver, amount)
    blockchain.append(new_block)
    previous_block = new_block
    return jsonify({'status': 'Transaction added successfully!'})

@app.route('/tamper_transaction', methods=['POST'])
def tamper_transaction():
    index = request.json.get('index')
    new_sender = request.json.get('sender')
    new_receiver = request.json.get('receiver')
    new_amount = request.json.get('amount')
    if 0 <= index < len(blockchain):
        blockchain[index].sender = new_sender
        blockchain[index].receiver = new_receiver
        blockchain[index].amount = new_amount
        recalculate_hashes()
        return jsonify({'status': 'Transaction tampered successfully!', 'tampered_blocks': [block.index for block in blockchain if block.is_tampered]})
    return jsonify({'status': 'Invalid block index!'}), 400

@app.route('/update_transaction', methods=['POST'])
def update_transaction():
    index = request.json.get('index')
    new_sender = request.json.get('sender')
    new_receiver = request.json.get('receiver')
    new_amount = request.json.get('amount')
    if 0 <= index < len(blockchain):
        blockchain[index].sender = new_sender
        blockchain[index].receiver = new_receiver
        blockchain[index].amount = new_amount
        recalculate_hashes()
        return jsonify({'status': 'Transaction updated successfully!', 'updated_blocks': [block.index for block in blockchain]})
    return jsonify({'status': 'Invalid block index!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
