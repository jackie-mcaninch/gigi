from bitarray import bitarray
import os
import sys

file_name = "vault.bin"
input = open(file_name, "rb")
out = open("records.txt","w")
file_size = os.stat(file_name).st_size
num_records = (file_size-1024)//32
out.write(f"TOTAL RECORDS IN FILE: {str(num_records)}\n\n")

#PRINT HEADER INFORMATION
wa = str(input.read(32).decode("utf8"))
ma = str(input.read(12).decode("utf8"))
ma = "-".join(ma[x:x+2] for x in range(0,len(ma),2))
out.write(f"wallet address is: {wa}\n")
out.write(f"mac address is: {ma}\n")
out.write("\n")
input.seek(1024, 0)

#PRINT INDIVIDUAL RECORDS
if len(sys.argv) > 1:
    if str(sys.argv[1])=="tail":
        if len(sys.argv) > 2:
            num_print = int(sys.argv[2])
        else:
            num_print = 20
        input.seek(-(num_print*32), 2)
    else:
        num_print = int(sys.argv[1])
else:
    num_print = 20
bits = bitarray(endian='big')
for i in range(num_print):
    in_bytes = input.read(24)
    bits.frombytes(in_bytes)
    bitstring = bits.to01()
    hex_hash = in_bytes.hex()
    n = int.from_bytes(input.read(4), "little")
    ts = int.from_bytes(input.read(4), "little")
    #out.write(f"{hex_hash:70s}\n")
    #out.write(f"{n:10d}  {ts:10d}  {bitstring:35s} {hex_hash:70s}\n")
    out.write(f"{n:10d}  {ts:10d}  {hex_hash:70s}\n")
    bits.clear()
    
input.close()
out.close()