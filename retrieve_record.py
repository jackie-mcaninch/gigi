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

def calc_expected_loc(val, f_size):
    loc_index = (val)/(2**256)
    s = int(loc_index*(f_size - 46))
    s -= s % 40
    s += 46
    return s

def retrieve(vault_name, bit_string, diff):
    #init challenge specific variables
    challenge = bitarray(bit_string)
    key = challenge[:diff]
    print("key is",key)
    int_rep = bitarray_to_int(challenge)
    file_name = "vaults/"+vault_name
    file_size = os.stat(file_name).st_size
    start_pt = calc_expected_loc(int_rep, file_size)
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
            print(i,"No")
            return False



import sys
import os
import random
from bitarray import bitarray




writer = open("random_challenge.txt","w")
for i in range(256):
    writer.write(str(random.randint(0,1)))
writer.close()
reader = open("random_challenge.txt","r")
#reader = open("sample_challenge.txt","r")
challenge_message = str(reader.read(256))
retrieve("testing.bin", challenge_message, int(sys.argv[1]))
reader.close()