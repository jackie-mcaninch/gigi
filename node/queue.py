from transaction import Transaction


class Queue:
    def __init__(self):
        self.queue = []
        self.add_transaction_message_to_queue("zyx124", "abd298", 4)
        self.add_transaction_message_to_queue("rtf345", "abd298", 4)
        self.add_transaction_message_to_queue("hre529", "abd298", 4)
        self.add_transaction_message_to_queue("bbg027", "abd298", 4)

    def add_transaction_message_to_queue(self, source_wallet, destination_wallet, num_coins):
        self.queue.append(Transaction(source_wallet, destination_wallet, num_coins).message)

    def remove_first_message(self):
        return self.queue.pop(0)

    def print_queue(self):
        i = 0
        print("Printing queue:")
        for message in self.queue:
            print("Message " + str(i) + ": " + str(message))
            i += 1

    def retrieve_all_messages(self):
        return self.queue

# this_queue = Queue()
# # message1 = Message("zyx124", "abd298", 4)
#
# this_queue.print_queue()
# print()
# print("Removing message: " + str(this_queue.remove_first_message()))
# print()
# this_queue.print_queue()