import random
from collections import defaultdict


class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.data = {}
        self.is_leader = False


class DistributedKeyValueStore:
    def __init__(self, num_nodes=5, replication_factor=3):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.replication_factor = min(replication_factor, num_nodes)
        self.leader = random.choice(self.nodes)
        self.leader.is_leader = True
        self.partition_map = defaultdict(list)

    def hash_key(self, key):
        return hash(key) % len(self.nodes)

    def put(self, key, value):
        primary_node = self.hash_key(key)
        nodes_to_update = self.get_replica_nodes(primary_node)

        for node in nodes_to_update:
            self.nodes[node].data[key] = value

        self.partition_map[primary_node].append(key)
        return f"Key '{key}' stored on nodes: {nodes_to_update}"

    def get(self, key):
        primary_node = self.hash_key(key)
        nodes_to_check = self.get_replica_nodes(primary_node)

        for node in nodes_to_check:
            if key in self.nodes[node].data:
                return f"Value for key '{key}': {self.nodes[node].data[key]}"

        return f"Key '{key}' not found"

    def get_replica_nodes(self, primary_node):
        return [
            (primary_node + i) % len(self.nodes)
            for i in range(self.replication_factor)
        ]

    def rebalance(self):
        avg_keys_per_node = sum(len(keys) for keys in self.partition_map.values()) / len(self.nodes)
        overloaded_nodes = [
            node for node, keys in self.partition_map.items()
            if len(keys) > avg_keys_per_node * 1.2
        ]
        underloaded_nodes = [
            node for node in range(len(self.nodes))
            if node not in overloaded_nodes
        ]

        for overloaded_node in overloaded_nodes:
            while len(self.partition_map[overloaded_node]) > avg_keys_per_node:
                key_to_move = self.partition_map[overloaded_node].pop()
                target_node = random.choice(underloaded_nodes)
                self.partition_map[target_node].append(key_to_move)

                # Update data on nodes
                value = self.nodes[overloaded_node].data[key_to_move]
                self.nodes[target_node].data[key_to_move] = value
                del self.nodes[overloaded_node].data[key_to_move]

        return "Rebalancing complete"

    def simulate_node_failure(self, node_id):
        failed_node = self.nodes[node_id]
        failed_node.data.clear()
        if failed_node.is_leader:
            failed_node.is_leader = False
            new_leader = random.choice([node for node in self.nodes if node.id != node_id])
            new_leader.is_leader = True
            self.leader = new_leader
        return f"Node {node_id} failed. New leader: Node {self.leader.id}"

    def repair_node(self, node_id):
        node_to_repair = self.nodes[node_id]
        for key in self.partition_map[node_id]:
            for other_node in self.get_replica_nodes(node_id):
                if key in self.nodes[other_node].data:
                    node_to_repair.data[key] = self.nodes[other_node].data[key]
                    break
        return f"Node {node_id} repaired"


# Example usage
store = DistributedKeyValueStore(num_nodes=5, replication_factor=3)

print(store.put("key1", "value1"))
print(store.put("key2", "value2"))
print(store.get("key1"))
print(store.get("key2"))

print(store.rebalance())

print(store.simulate_node_failure(0))
print(store.repair_node(0))