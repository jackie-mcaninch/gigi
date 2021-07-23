import random

class Vault:
    @staticmethod
    def does_hash_exist_on_disk(this_hash, difficulty):
        flip = random.randint(0, 1)
        if flip == 0:
            print("True - " + str(this_hash) + " does exist on disk with difficulty " + str(difficulty))
        else:
            print("False - " + str(this_hash) + " does NOT exist on disk with difficulty " + str(difficulty))


v = Vault()
v.does_hash_exist_on_disk("123abc", 20)
v.does_hash_exist_on_disk("456yhg", 20)
v.does_hash_exist_on_disk("321kij", 20)
v.does_hash_exist_on_disk("984rty", 20)
v.does_hash_exist_on_disk("345oop", 20)
v.does_hash_exist_on_disk("239iio", 20)
v.does_hash_exist_on_disk("879jhd", 20)
v.does_hash_exist_on_disk("306vcp", 20)
