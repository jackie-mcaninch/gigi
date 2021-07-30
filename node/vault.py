import random
import sys
import os
import mmh3
import time
from bitarray import bitarray
from kafka import KafkaProducer

class Vault:
    def __init__(self):
        #SYNTAX: python vault.py find <hash> <difficulty> <block_size (optional)>
        if len(sys.argv) > 2:
            if sys.argv[1] == "find":
                block_size = 4000
                if len(sys.argv)>4:
                    block_size = int(sys.argv[4])
                print("Searching for hash of difficulty",sys.argv[3],"and block size",block_size)
                
                #consult filter and retrieve
                if int(sys.argv[3]) != 25:
                    print("Filter does not support variable difficulties yet... skipping initial check")
                    self.retrieve("full_vault.bin",sys.argv[2], int(sys.argv[3]), block_size)
                else:   
                    if self.check_filter(sys.argv[2], int(sys.argv[3])):
                        print("filter says record exists")
                        self.retrieve("full_vault.bin",sys.argv[2], int(sys.argv[3]), block_size)
                    else:
                        print("filter says record does not exist")
                    print("\n")

    # def does_hash_exist_on_disk(self, this_hash, difficulty):
        # self.retrieve("testing.bin", this_hash, difficulty)
        # flip = random.randint(0, 1)
        # if flip == 0:
        #     print("True - " + str(this_hash) + " does exist on disk with difficulty " + str(difficulty))
        # else:
        #     print("False - " + str(this_hash) + " does NOT exist on disk with difficulty " + str(difficulty))

    def check_filter(self, target_rec, diff):
        target_rec = bitarray(target_rec,endian="big")
        fil = open("../vaults/current-filter-"+str(diff)+".bin", "rb")
        filter = bitarray(endian="big")
        filter.frombytes(fil.read(10485728))
        digest1 = mmh3.hash(target_rec[:diff].tobytes(), 1) % len(filter)
        digest2 = mmh3.hash(target_rec[:diff].tobytes(), 2) % len(filter)
        if filter[digest1] == 1 and filter[digest2] == 1:
            return True
        return False
    
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

    
    def retrieve(self, vault_name, bit_string, diff, block_size):
        #init challenge specific variables
        bit_string = bit_string.ljust(256, "0")
        challenge = bitarray(bit_string)
        key = challenge[:diff]
        int_rep = self.bitarray_to_int(challenge)
        file_name = "../vaults/"+vault_name
        file_size = os.stat(file_name).st_size
        start_pt = max(46, self.calc_expected_loc(int_rep, file_size)-(block_size//2))
        # print("start pt is",start_pt)

        #init searching tools
        seeker = open(file_name, "rb")
        seeker.seek(start_pt)
        first_record = bitarray(endian="big")
        last_record = bitarray(endian="big")

        #locate correct block
        s1 = time.time()
        while True:
            # print("fp is",seeker.tell())
            first_record.clear()
            last_record.clear()
            buf = bytes(seeker.read(min(block_size, file_size-seeker.tell())))
            first_record.frombytes(buf[0:32])
            if first_record[:diff]>key:
                if seeker.tell() <= block_size+46:
                    #file lower bound reached
                    e1 = time.time()
                    print(f"TOTAL TIME FOR DISK SEARCHING: {e1-s1:.4f} seconds")
                    return False
                seeker.seek(max(-(2*block_size), -(seeker.tell()-46)), 1)
                continue
            last_record.frombytes(buf[-40:-8])
            if last_record[:diff]<key:
                if seeker.tell()==file_size:
                    #file upper bound reached
                    e1 = time.time()
                    print(f"TOTAL TIME FOR DISK SEARCHING: {e1-s1:.4f} seconds")
                    return False
                continue
            e1 = time.time()
            print(f"TIME FOR DISK SEARCHING: {e1-s1:.4f} seconds")
            break

        #begin binary search on block
        s2 = time.time()
        hi = len(buf)
        lo = 0
        elem = bitarray(endian="big")
        while lo <= hi:
            #set search vars
            elem.clear()
            mid = int((lo + (hi-lo) // 2)//40)*40
            elem.frombytes(buf[mid:mid+32])
            
            #found the record
            if elem[:diff] == key:
                e2 = time.time()
                print(f"TIME FOR BINARY SEARCH: {e2-s2:.4f} seconds")
                print(f"TOTAL TIME FOR RECORD RETRIEVAL: {e2-s1:.4f} seconds")
                print("***success***")
                return buf[mid:mid+40]

            #else move pointer
            elif elem[:diff] < key:
                lo = mid + 40
            else:
                hi = mid -40

        #element does not exist
        e2 = time.time()
        print(f"TIME FOR BINARY SEARCH: {e2-s2:.4f} seconds")
        print(f"TOTAL TIME FOR RECORD RETRIEVAL: {e2-s1:.4f} seconds")
        return False

    def create_message(self, vault_name, rec, n, ts):
        reader = open(vault_name, "rb")
        head = reader.read(46)
        reader.close()
        tail = bytes(n+ts+rec)
        full_msg = head+tail
        #p = KafkaProducer(bootstrap_servers='localhost:9092')
        #p.send('gigi_winners', key=b'win msg', value=full_msg)
        #p.close()
        print(full_msg)



v = Vault()
