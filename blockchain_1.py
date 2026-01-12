import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # attendance data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        print(f"⛏ Mining block {self.index} with difficulty {difficulty}...")
        target = "0" * difficulty
        start = time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        end = time()
        mining_time = end - start
        print(f"✅ Block mined: {self.hash}")
        print(f"⏱ Mining time: {mining_time:.3f} seconds")
        return mining_time


class Blockchain:
    def __init__(self):
        self.difficulty = 3
        self.chain = [self.create_genesis_block()]
        self.attendance_log = {}  # Prevent duplicate attendance

    def create_genesis_block(self):
        genesis = Block(0, time(), "Genesis Block - Attendance Ledger", "0")
        genesis.mine_block(self.difficulty)
        return genesis

    def get_latest_block(self):
        if not self.chain:
            # Safety check
            self.chain = [self.create_genesis_block()]
        return self.chain[-1]

    def add_block(self, data):
        student = data.get("student")
        date = data.get("date")
        key = f"{student}-{date}"

        if key in self.attendance_log:
            return {"error": "Attendance already marked for this student today"}, 409

        previous = self.get_latest_block()
        new_block = Block(len(self.chain), time(), data, previous.hash)
        mining_time = new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        # Save attendance
        self.attendance_log[key] = True

        return {"success": True, "mining_time": mining_time}, 201

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i - 1]
            if cur.hash != cur.calculate_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
        return True
