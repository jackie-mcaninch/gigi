import time
import hashlib
import json
from queue import Queue
from blockchain import Blockchain

class Block:
    def __init__(self):
        self.block_header = {}
        self.block = {}

    def create_block(self):
        block_data = self.get_block_data()
        hash_of_previous_block_header = self.get_hash_of_previous_block_header()
        self.create_block_header(hash_of_previous_block_header, block_data)
        self.block['block_header'] = self.block_header
        self.block['block_data'] = block_data
        return self.block

    def create_block_header(self, hash_of_previous_block_header, block_data):
        self.block_header['previous_block_header'] = hash_of_previous_block_header
        self.block_header['timestamp'] = time.time()
        self.block_header['hash_of_block_data'] = hashlib.sha256(json.dumps(block_data).encode('utf-8')).hexdigest()

    def get_block_data(self):
        block_data = self.get_all_messages_from_queue()
        return block_data

    def get_all_messages_from_queue(self):
        queue = Queue()
        return queue.retrieve_all_messages()

    def get_hash_of_previous_block_header(self):
        bc = Blockchain()
        return bc.get_previous_block_hash()


# TODO confirm with blockchain that a wallet has num_coins before allowing transaction

b = Block()
b.create_block()