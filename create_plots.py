class Record:
    def __init__(self, idx, ts):
        self.index = idx
        self.timestamp = ts
        self.hash_val = None

    def create_hash(self, h):
        h.update(self.timestamp.to_bytes(32, "big"))
        h.update(self.index.to_bytes(32, "big"))
        self.hash_val = h.digest()

    def __lt__(self, other):
        if self.hash_val < other.hash_val:
            return True
        return False
    #used for testing only - delete after
    def __repr__(self):
        return str(int.from_bytes(self.val, "big"))+"    "+str(self.id)

def sort_records(rlst):
    pass

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

#record level
nonce = 0
timestamp = None



#GENERATION

record_lst = [None]*1000000#26843538
s = time.time()
h = hashlib.sha256()
h.update(wallet_addr)
h.update(mac_addr)
h.update(process_id)
h.update(vault_id)
while nonce<len(record_lst):
    timestamp = int(time.time())
    record_lst[nonce] = Record(nonce, timestamp)
    record_lst[nonce].create_hash(h.copy())
    nonce += 1
e = time.time()

print(f"TOTAL TIME FOR GENERATION: {e-s:.4f} seconds")

#SORTING
r2 = numpy.array(record_lst)
s = time.time()
r2.sort(kind="mergesort")
e = time.time()
print(f"TOTAL TIME FOR NP INPLACE MERGESORT: {e-s:.4f} seconds")

#WRITING
s = time.time()

#total memory for file header is 256 + 6 + 4 + 4 = 270 bytes
os.chdir("vaults")
file_name = "testing.bin"#str(vault_id)+".bin"
writer = open(file_name, "wb")
writer.write(int.from_bytes(wallet_addr, "big").to_bytes(256, "big"))
writer.write(mac_addr)
writer.write(process_id)
writer.write(vault_id)

#total memory for every record is 4 + 4 + 32 = 40 bytes
for rec in record_lst:
    writer.write(rec.index.to_bytes(4, "big"))
    writer.write(rec.timestamp.to_bytes(4, "big"))
    writer.write(rec.hash_val)
writer.close()
e = time.time()
print(f"TOTAL TIME FOR WRITING: {e-s:.4f} seconds")

