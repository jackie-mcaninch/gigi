import json
import time


class Transaction:
    def __init__(self, source_wallet, destination_wallet, num_coins):
        self.message = {}
        self.add_or_update_source_wallet(source_wallet)
        self.add_or_update_destination_wallet(destination_wallet)
        self.add_or_update_transaction_num_coins(num_coins)
        self.add_or_update_timestamp(time.time())
        self.add_or_update_message_version()

    def convert_message_to_json(self):
        self.message = json.dumps(self.message)

    def add_or_update_source_wallet(self, source_wallet):
        self.message['source_wallet'] = source_wallet

    def add_or_update_destination_wallet(self, destination_wallet):
        self.message['destination_wallet'] = destination_wallet

    def add_or_update_transaction_num_coins(self, num_coins):
        self.message['num_coins'] = num_coins

    def add_or_update_timestamp(self, timestamp):
        self.message['timestamp'] = timestamp

    def add_or_update_message_version(self):
        self.message['message_version'] = 1.0


# Message items:
# Source Wallet ID
# Destination Wallet ID
# Transaction Amount
# Timestamp
# Message Version
#
#