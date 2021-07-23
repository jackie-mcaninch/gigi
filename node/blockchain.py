from pathlib import Path
import numpy as np

class Blockchain:
    def __init__(self):
        # retrieve blockchain from disk
        blockchain_file = Path("blockchain.npy")

        # if blockchain file does not exist then retrieve it from another node
        if not blockchain_file.is_file():
            self.download_blockchain()

        # if blockchain file exists then open the file and store it in memory
        self.blockchain = np.load('blockchain.npy',allow_pickle='TRUE').item()

    @staticmethod
    def download_blockchain():
        # TODO update this function to download blockchain from another node
        temp_dict = {}

        # this line only exists to initiate the genesis block. It should only run on the first node created and never again be used
        temp_dict['0000000000000000000000000000000000000000000000000000000000000000'] = {}

        # this line will stay even after updating the above lines to actually retrieve the blockchain from another node
        np.save('blockchain.npy', temp_dict)
        # f = open("blockchain.npy", "a")
        # f.write()

    def add_block(self):
        # retrieve new block
        new_block = self.retrieve_new_block()

        # add new block to hashmap
        self.blockchain[new_block['block_header']['hash_of_block_data']] = new_block

        # save hashmap to disk
        np.save('blockchain.npy', self.blockchain)

    @staticmethod
    def retrieve_new_block():
        from block import Block
        b = Block()
        return b.create_block()

    def return_entire_blockchain(self):
        # this function can be called to send the entire blockchain to a new node.
        return self.blockchain

    def get_previous_block_hash(self):
        return list(self.blockchain)[-1]


b = Blockchain()
print("last block:")
print(b.get_previous_block_hash())
b.add_block()
print("entire blockchain:")
print(b.return_entire_blockchain())
