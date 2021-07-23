import random
import sys
import os
from bitarray import bitarray

class Vault:
    def does_hash_exist_on_disk(self, this_hash, difficulty):
        self.retrieve("testing.bin", this_hash, difficulty)
        # flip = random.randint(0, 1)
        # if flip == 0:
        #     print("True - " + str(this_hash) + " does exist on disk with difficulty " + str(difficulty))
        # else:
        #     print("False - " + str(this_hash) + " does NOT exist on disk with difficulty " + str(difficulty))

    def bitarray_to_int(self, arr):
        total = 0
        for i in range(1,len(arr)+1):
            total += (arr[-i])*(2**(i-1))
        return total
    
    
    def calc_expected_loc(self, val, f_size):
        loc_index = (val)/(2**256)
        s = int(loc_index*(f_size - 46))
        s -= s % 40
        s += 46
        return s

    
    def retrieve(self, vault_name, bit_string, diff):
        #init challenge specific variables
        challenge = bitarray(bit_string)
        key = challenge[:diff]
        print("key is",key)
        int_rep = self.bitarray_to_int(challenge)
        file_name = "../vaults/"+vault_name
        file_size = os.stat(file_name).st_size
        start_pt = self.calc_expected_loc(int_rep, file_size)
        #print("starting point is",start_pt)

        #init searching tools
        seeker = open(file_name, "rb")
        seeker.seek(start_pt)
        record = bitarray(endian="big")
        is_right = False
        is_left = False

        i=0
        #begin search
        while True:
            i+=1
            record.clear()
            #seeker.read(4000)
            record.frombytes(seeker.read(32))
            n = int.from_bytes(seeker.read(4), "big")
            ts = int.from_bytes(seeker.read(4), "big")
            #success case
            if record[:diff]==key:
                #print(i,"Yes")
                print(f"success! found after {i:4d} iterations {n:10d}  {ts:10d}  {repr(record[:diff]):300s}")
                return True
            #keep searching case
            else:
                if record[:diff]<key and is_left==False and seeker.tell()<file_size:
                    is_right = True
                    continue
                elif record[:diff]>key and is_right==False and seeker.tell()>310:
                    is_left = True
                    #decrement file pointer
                    seeker.seek(-80,1)
                    continue
                print("record does not exist")
                return False            


v = Vault()
v.does_hash_exist_on_disk("0000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000011111", 50)
