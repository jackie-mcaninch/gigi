from bitarray import bitarray
import os
import sys

file_name = "vault.bin"
#file_name2 = "vault2.bin"
input = open(file_name, "rb")
#input2 = open(file_name2, "rb")
out = open("records2.txt","w")
#out2 = open("records2.txt","w")
file_size = os.stat(file_name).st_size
num_records = (file_size)//32
out.write(f"TOTAL RECORDS IN FILE: {str(num_records)}\n")

#PRINT HEADER INFORMATION
# wa = str(input.read(32).decode("utf8"))
# ma = str(int.from_bytes(input.read(6), "big"))
# pid = str(int.from_bytes(input.read(4), "big"))
# vid = str(int.from_bytes(input.read(4), "big"))
# out.write(f"wallet address is: {wa}\n")
# out.write(f"mac address is: {ma}\n")
# out.write(f"process id is: {pid}\n")
# out.write(f"vault id is: {vid}\n")
# out.write("\n")

#PRINT INDIVIDUAL RECORDS (SORTED BY HASH VALUE)
if len(sys.argv) > 1:
    num_print = int(sys.argv[1])
else:
    num_print = 20
bits = bitarray(endian='big')
for i in range(num_print):
    in_bytes = input.read(32)
    bits.frombytes(in_bytes)
    bitstring = bits.to01()
    hex_hash = in_bytes.hex()
    # n = int.from_bytes(input.read(4), "big")
    # ts = int.from_bytes(input.read(4), "big")
    out.write(f"{hex_hash:70s}\n")
    # out.write(f"{n:10d}  {ts:10d}  {bitstring:35s} {hex_hash:70s}\n")
    bits.clear()

    # in_bytes = input2.read(32)
    # bits.frombytes(in_bytes)
    # bitstring = bits.to01()
    # hex_hash = in_bytes.hex()
    # out2.write(f"{hex_hash:70s}\n")
    # bits.clear()
    
input.close()
#input2.close()
out.close()
#out2.close()