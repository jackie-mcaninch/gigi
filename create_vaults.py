#DEFINE STATIC FUNCTIONS
def get_existing_vaults():
    num_existing_vaults = 0
    try:
        os.chdir("vaults")
    except:
        os.mkdir("vaults")
        os.chdir("vaults")
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file[-4:]==".bin" and file!="filters.bin":
                num_existing_vaults += 1
    os.chdir("../")
    return num_existing_vaults



#IMPORT PYTHON MODULES (REMEMBER USER MUST INSTALL ALL)
import random
import sys
import os
import time
import hashlib
import bloom
import uuid
import numpy
import io


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
num_records = int(sys.argv[1])
hash_vals = numpy.empty(num_records, dtype=numpy.dtype('V32'))
print("Number of records:", num_records)
timestamps = {}
nonces = {}

#start timer (testing only)
s = time.time()

#init vault-specific info
header_bytes = bytes(wallet_addr + mac_addr + process_id + vault_id)
h = hashlib.sha256()
h.update(header_bytes)

#create records
while nonce<len(hash_vals)-1:  
    #update nonce and timestamp
    nonce += 1
    timestamp = int(time.time())
    record_bytes = nonce.to_bytes(4, "big") + timestamp.to_bytes(4, "big")
    #store hash and corresponding timestamps/nonce
    h2 = h.copy()
    h2.update(record_bytes)
    hash_vals[nonce] = h2.digest()
    nonces[bytes(hash_vals[nonce])] = nonce 
    timestamps[bytes(hash_vals[nonce])] = timestamp
#stop timer (testing only)
e = time.time()
print(f"TOTAL TIME FOR GENERATION: {e-s:.4f} seconds")



#SORTING

#start timer (testing only)
s = time.time()

#sort hash values
hash_vals.sort(kind="mergesort")

#stop timer (testing only)
e = time.time()
print(f"TOTAL TIME FOR SORTING: {e-s:.4f} seconds")


#WRITING

#start timer (testing only)
s = time.time()

#write file header
#total mem: 256 + 6 + 4 + 4 = 270 bytes
os.chdir("vaults")
file_name = "testing.bin"#str(vault_id)+".bin"
writer = open(file_name, "wb")
#print(io.DEFAULT_BUFFER_SIZE)
writer.write(wallet_addr)#int.from_bytes(wallet_addr, "big").to_bytes(32, "big"))
writer.write(mac_addr)
writer.write(process_id)
writer.write(vault_id)

#write all records
#total mem: 32 + 4 + 4 = 40 bytes per record
#index = 0
#while index < len(hash_vals):
#    line = bytearray(100000*40)
#    line_idx = 0
#    for val in hash_vals[index:min(len(hash_vals)-1, index+100000)]:
#        line[line_idx:line_idx+32] = bytes(val)
#        line_idx += 32
#        line[line_idx:line_idx+4] = nonces[bytes(val)].to_bytes(4, "big")
#        line_idx += 4
#        line[line_idx:line_idx+4] = timestamps[bytes(val)].to_bytes(4, "big")
#        line_idx +=4
#        #line += bytes(val) + nonces[bytes(val)].to_bytes(4, "big") + timestamps[bytes(val)].to_bytes(4, "big")
#    writer.write(bytes(line))
#    index += 100000
for val in hash_vals:
    line = bytes(val) + nonces[bytes(val)].to_bytes(4, "big") + timestamps[bytes(val)].to_bytes(4, "big")
    writer.write(line)
writer.close()

#end timer (testing only)
e = time.time()
print(f"TOTAL TIME FOR WRITING: {e-s:.4f} seconds")

