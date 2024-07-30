from flask import Flask, jsonify, request, render_template
import hashlib
import time

app = Flask(__name__)

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, is_tampered=False):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.is_tampered = is_tampered  # Flag to indicate tampering

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

def recalculate_hashes():
    tampered_blocks = []
    for i in range(len(blockchain)):
        if i == 0:
            blockchain[i].hash = calculate_hash(blockchain[i].index, blockchain[i].previous_hash, blockchain[i].timestamp, blockchain[i].data)
        else:
            new_hash = calculate_hash(blockchain[i].index, blockchain[i].previous_hash, blockchain[i].timestamp, blockchain[i].data)
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
            'data': block.data,
            'hash': block.hash,
            'is_tampered': block.is_tampered
        })
    return jsonify(chain)

@app.route('/add_block', methods=['POST'])
def add_block():
    global previous_block
    data = request.json.get('data', '')
    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)
    previous_block = new_block
    return jsonify({'status': 'Block added successfully!'})

@app.route('/tamper_block', methods=['POST'])
def tamper_block():
    index = request.json.get('index')
    new_data = request.json.get('data')
    if 0 <= index < len(blockchain):
        blockchain[index].data = new_data
        recalculate_hashes()
        return jsonify({'status': 'Block tampered successfully!', 'tampered_blocks': [block.index for block in blockchain if block.is_tampered]})
    return jsonify({'status': 'Invalid block index!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
