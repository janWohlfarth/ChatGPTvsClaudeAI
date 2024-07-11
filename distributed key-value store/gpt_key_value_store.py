from flask import Flask, request, jsonify
import redis
import hashlib
import threading
import random

app = Flask(__name__)

# Configuration
NUM_NODES = 3
REPLICATION_FACTOR = 2

# Nodes in the system
nodes = []
leaders = {}

# Redis clients for each node
redis_clients = {}

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.address = f"node_{node_id}"
        self.is_leader = False
        redis_clients[self.node_id] = redis.Redis(host='localhost', port=6379 + self.node_id, db=0)

# Initialize nodes
for i in range(NUM_NODES):
    nodes.append(Node(i))

def hash_key(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)

def get_node_for_key(key):
    hashed_key = hash_key(key)
    return nodes[hashed_key % NUM_NODES]

def replicate_key(key, value):
    for i in range(REPLICATION_FACTOR):
        node = nodes[(hash_key(key) + i) % NUM_NODES]
        redis_clients[node.node_id].set(key, value)

@app.route('/put', methods=['PUT'])
def put_key():
    key = request.json['key']
    value = request.json['value']
    node = get_node_for_key(key)
    if node.is_leader:
        redis_clients[node.node_id].set(key, value)
        replicate_key(key, value)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failure", "message": "Not the leader"}), 400

@app.route('/get/<key>', methods=['GET'])
def get_key(key):
    node = get_node_for_key(key)
    value = redis_clients[node.node_id].get(key)
    if value:
        return jsonify({"key": key, "value": value.decode()})
    else:
        return jsonify({"status": "failure", "message": "Key not found"}), 404

def elect_leader():
    leader = random.choice(nodes)
    leader.is_leader = True
    leaders[leader.node_id] = leader
    print(f"Leader elected: {leader.node_id}")

@app.before_first_request
def initialize():
    elect_leader()

if __name__ == '__main__':
    app.run(port=5000)
