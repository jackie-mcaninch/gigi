#DEFINE STATIC FUNCTIONS
def get_existing_vaults():
    num_existing_vaults = 0
    try:
        os.chdir("vaults")
    except:
        os.mkdir("vaults")
        os.chdir("vaults")
    for _, _, files in os.walk(os.getcwd()):
        for file in files:
            if file[-4:]==".bin":
                num_existing_vaults += 1
    os.chdir("../")
    return num_existing_vaults



#IMPORT PYTHON MODULES (REMEMBER USER MUST INSTALL ALL)
import random
import sys
import os
import time
import hashlib
import uuid
import numpy
import io
from filter import filter


#UNIQUE ATTRIBUTES FOR HASHING

#node level
wallet_addr = int.from_bytes(bytes("get-from-wallet", encoding="utf8"), "big").to_bytes(32, "big")
mac_addr = uuid.getnode().to_bytes(6, "big")

#vault level
process_id = os.getpid().to_bytes(4, "big")
vault_id = (get_existing_vaults()+1).to_bytes(4, "big")

#record level
nonce = -1
timestamp = None


#GENERATION

#init array of hashes and dictionaries
if len(sys.argv) > 1:
    num_records = int(sys.argv[1])
else:
    num_records = 26843544
hash_vals = numpy.empty(num_records, dtype=numpy.dtype('V32'))
print("Number of records:", num_records)
other_info = {}

#start timer (testing only)
s = time.time()

#init vault-specific info
header_bytes = bytes(wallet_addr + mac_addr + process_id + vault_id)
h = hashlib.sha256()
h.update(header_bytes)

#create records
#parsl
while nonce<len(hash_vals)-1:  
    #update nonce and timestamp
    nonce += 1
    timestamp = int(time.time())
    record_bytes = nonce.to_bytes(4, "big") + timestamp.to_bytes(4, "big")
    #store hash and corresponding timestamps/nonce
    h2 = h.copy()
    h2.update(record_bytes)
    hash_vals[nonce] = h2.digest()
    other_info[bytes(hash_vals[nonce])] = (nonce, timestamp)


#stop timer (testing only)
e = time.time()
print(f"TOTAL TIME FOR GENERATION: {e-s:.4f} seconds")



#SORTING

#start timer (testing only)
s = time.time()

#sort hash values
hash_vals.sort(kind="quicksort") #for future mods, maybe try tensorflow sort with parallelization

#stop timer (testing only)
e = time.time()
print(f"TOTAL TIME FOR SORTING: {e-s:.4f} seconds")


#WRITING

#start timer (testing only)
s = time.time()

#write file header
#total mem: 32 + 6 + 4 + 4 = 46 bytes
os.chdir("vaults")
file_name = "full_vault.bin"
#buf_size = io.DEFAULT_BUFFER_SIZE
writer = open(file_name, "wb", -1)#, buf_size)
writer.write(wallet_addr)
writer.write(mac_addr)
writer.write(process_id)
writer.write(vault_id)
writer.flush()

#write all records
#total mem: 32 + 4 + 4 = 40 bytes per record

# ***implement later: manipulate file buffering to optimize***
# index = 0
# while index < len(hash_vals):
#     line = bytearray(100000*40)
#     line_idx = 0
#     for val in hash_vals[index:min(len(hash_vals)-1, index+100000)]:
#         line[line_idx:line_idx+32] = bytes(val)
#         line_idx += 32
#         line[line_idx:line_idx+4] = other_info[bytes(val)][0].to_bytes(4, "big")
#         line_idx += 4
#         line[line_idx:line_idx+4] = other_info[bytes(val)][1].to_bytes(4, "big")
#         line_idx +=4
#     writer.write(bytes(line))
#     writer.flush()
#     index += 100000

for val in hash_vals:
   line = bytes(val) + other_info[bytes(val)][0].to_bytes(4, "big") + other_info[bytes(val)][1].to_bytes(4, "big")
   writer.write(line)
writer.close()

#end timer (testing only)
e = time.time()
print(f"TOTAL TIME FOR WRITING: {e-s:.4f} seconds")


#BUILD FILTER

#start timer (testing only)
s = time.time()

#add filter items
f = filter()
f.add_filter(file_name,25)
f.clean_filters(25)

#end timer (testing only)
e = time.time()
print(f"TOTAL TIME FOR BUILDING FILTER: {e-s:.4f} seconds")