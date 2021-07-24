#establish target... from args? or file?
#comb through filter file
#mark every file that is flagged
#find starting point (uniform distribution)
#perform binary search
#write vault message

import sys
import os
import random
from bitarray import bitarray

def bitarray_to_int(arr):
    total = 0
    for i in range(1,len(arr)+1):
        total += (arr[-i])*(2**(i-1))
    return total

def calc_expected_loc(val, f_size):
    loc_index = (val)/(2**256)
    s = int((loc_index*(f_size - 46)))
    s -= s % 40
    s += 46
    if s==f_size:
        s -= 40 #move to very last record
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







writer = open("random_challenge.txt","w")
for i in range(256):
   writer.write(str(random.randint(0,1)))
writer.close()
#reader = open("random_challenge.txt","r")
reader = open("sample_challenge.txt","r")
challenge_message = str(reader.read(256))
retrieve("testing.bin", challenge_message, int(sys.argv[1]))
reader.close()