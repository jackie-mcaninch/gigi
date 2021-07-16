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


#UNIQUE ATTRIBUTES FOR HASHING

#node level
wallet_addr = bytes("get-from-wallet", encoding="utf8")
mac_addr = uuid.getnode().to_bytes(6, "big")
print("wallet address =", wallet_addr.decode("utf8"))
print("mac address =", int.from_bytes(mac_addr, "big"))

#vault level
process_id = os.getpid().to_bytes(4, "big")
vault_id = (get_existing_vaults()+1).to_bytes(4, "big")
print("pid =", int.from_bytes(process_id, "big"))
print("vid =", int.from_bytes(vault_id, "big"))
print("\n")

#record level
nonce = -1
timestamp = None


#GENERATION

#init array of hashes and dictionaries
hash_vals = numpy.empty(16, dtype=numpy.dtype('S32'))
timestamps = {}
nonces = {}

#start timer (testing only)
s = time.time()

#init vault-specific info
h = hashlib.sha256()
h.update(wallet_addr)
h.update(mac_addr)
h.update(process_id)
h.update(vault_id)

#create records
while nonce<len(hash_vals)-1:  
    #update nonce and timestamp
    nonce += 1
    timestamp = int(time.time())
    #generate hash
    h2 = h.copy()
    h2.update(timestamp.to_bytes(4, "big"))
    h2.update(nonce.to_bytes(4, "big"))
    hash_val = h2.digest()
    #store hash and corresponding timestamps/nonce
    hash_vals[nonce] = hash_val
    timestamps[hash_val] = timestamp
    nonces[hash_val] = nonce  

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
print(f"TOTAL TIME FOR NP INPLACE MERGESORT: {e-s:.4f} seconds")


#WRITING

#start timer (testing only)
s = time.time()

#write file header
#total mem: 256 + 6 + 4 + 4 = 270 bytes
os.chdir("vaults")
file_name = "testing.bin"#str(vault_id)+".bin"
writer = open(file_name, "wb")
writer.write(int.from_bytes(wallet_addr, "big").to_bytes(256, "big"))
writer.write(mac_addr)
writer.write(process_id)
writer.write(vault_id)

#write all records
#total mem: 32 + 4 + 4 = 40 bytes per record
for val in hash_vals:
    writer.write(val)
    writer.write(nonces[val].to_bytes(4, "big"))
    writer.write(timestamps[val].to_bytes(4, "big"))
writer.close()

#end timer (testing only)
e = time.time()
print(f"TOTAL TIME FOR WRITING: {e-s:.4f} seconds")

