#establish target... from args? or file?
#comb through filter file
#mark every file that is flagged
#find starting point (uniform distribution)
#perform binary search
#write vault message

def bitarray_to_int(arr):
    total = 0
    for i in range(1,len(arr)+1):
        total += (arr[-i])*(2**(i-1))
    return total

def retrieve(bit_string, diff):
    challenge = bitarray(bit_string)
    key = challenge[:diff]
    #print(key.tolist())
    int_rep = bitarray_to_int(key)
    maximum = (2**diff)
    loc_index = int_rep/maximum
    file_size = os.stat("vaults/testing.bin").st_size
    start_pt = int(loc_index*(file_size - 270))                 #find statistically probable location of record
    start_pt -= (start_pt % 40)                                 #round to nearest record start
    start_pt += 270                                             #skip file header
    #print("starting point is",start_pt)
    file_name = "vaults/testing.bin"
    seeker = open(file_name, "rb")
    seeker.seek(start_pt)
    record = bitarray(endian="big")
    is_right = False
    is_left = False
    for i in range(1000000): #simply to time out, adjust later
        #print(seeker.tell())
        record.clear()
        record.frombytes(seeker.read(32))
        n = int.from_bytes(seeker.read(4), "big")
        ts = int.from_bytes(seeker.read(4), "big")
        #success case
        if record[:diff]==key:
            print(i,"Yes")
            #print(f"{n:10d}  {ts:10d}  {repr(record[:diff]):300s}")
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
            print(i,"No")
            return False
    print("loop timed out")



import sys
import os
import random
from bitarray import bitarray



#reader = open("sample_challenge.txt","r")
writer = open("random_challenge.txt","w")
for i in range(256):
    writer.write(str(random.randint(0,1)))
writer.close()
reader = open("random_challenge.txt","r")
challenge_message = str(reader.read(256))
retrieve(challenge_message, int(sys.argv[1]))
reader.close()