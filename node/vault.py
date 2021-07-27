import random
import sys
import os
import json
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
        if s==f_size:
            s -= 40 #move to very last record
        return s

    
    def retrieve(self, vault_name, bit_string, diff):
        #init challenge specific variables
        bit_string = bit_string.ljust(256, "0")
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
        first_record = bitarray(endian="big")
        last_record = bitarray(endian="big")

        #locate correct block
        while True:
            print("file pos is", seeker.tell())
            first_record.clear()
            last_record.clear()
            buf = bytes(seeker.read(min(4000, file_size-seeker.tell())))
            first_record.frombytes(buf[0:32])
            if first_record[:diff]>key:
                if seeker.tell() <= 4046:
                    print("record does not exist")
                    return False
                seeker.seek(max(-8000, -(seeker.tell()-46)), 1)
                continue
            last_record.frombytes(buf[-40:-8])
            if last_record[:diff]<key:
                if seeker.tell()==file_size:
                    print("record does not exist")
                    return False
                continue
            print("found correct block!")
            break
        #begin binary search on block
        hi = len(buf)
        lo = 0
        elem = bitarray(endian="big")
        while lo <= hi:
            elem.clear()
            mid = int((lo + (hi-lo) // 2)//40)*40
            elem.frombytes(buf[mid:mid+32])
            if elem[:diff] == key:
                print("found correct record!")
                return buf[mid:mid+40]
            elif elem[:diff] < key:
                lo = mid + 40
            else:
                hi = mid -40
        print("element not found")
        return False

    def create_message(self, vault_name, rec, n, ts):
        reader = open(vault_name, "rb")
        head = reader.read(46)
        tail = bytes(n+ts+rec)
        full_msg = head+tail
        print(full_msg)
        #create JSON message to give to Kafka
        pass



v = Vault()
# scan filter file
# create list of possible vaults to search
# call below function on each match sequentially
v.does_hash_exist_on_disk("0"*256, 10)
