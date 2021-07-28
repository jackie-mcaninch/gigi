from bitarray import bitarray
import os

input = open("vaults/test.bin", "rb")
file_size = os.stat("vaults/test.bin").st_size
num_records = (file_size - 46)//40
print("TOTAL RECORDS IN FILE:",num_records)

#PRINT HEADER INFORMATION
wa = str(input.read(32).decode("utf8"))
ma = int.from_bytes(input.read(6), "big")
pid = int.from_bytes(input.read(4), "big")
vid = int.from_bytes(input.read(4), "big")
#print("wallet address is:", wa)
#print("mac address is:", ma)
#print("process id is:", pid)
#print("vault id is:", vid)
#print("\n")

#PRINT INDIVIDUAL RECORDS (SORTED BY HASH VALUE)
bits = bitarray(endian='big')
out = open("records.txt","w")
for i in range(500):
    in_bytes = input.read(32)
    bits.frombytes(in_bytes)
    bitstring = bits.to01()
    hex_hash = in_bytes.hex()
    n = int.from_bytes(input.read(4), "big")
    ts = int.from_bytes(input.read(4), "big")
    out.write(f"{n:10d}  {ts:10d}  {bitstring:35s} {hex_hash:70s}\n")
    bits.clear()
    
input.close()
