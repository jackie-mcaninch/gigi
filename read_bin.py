from bitarray import bitarray
input = open("vaults/testing.bin", "rb")

#PRINT HEADER INFORMATION
wa = str(input.read(256).decode("utf8"))
ma = int.from_bytes(input.read(6), "big")
pid = int.from_bytes(input.read(4), "big")
vid = int.from_bytes(input.read(4), "big")
print("wallet address is:", wa)
print("mac address is:", ma)
print("process id is:", pid)
print("vault id is:", vid)
print("\n")

#PRINT INDIVIDUAL RECORDS (SORTED BY HASH VALUE)
bits = bitarray(endian='big')
#out = open("records.txt","w")
for i in range(20):
    in_bytes = input.read(32)
    bits.frombytes(in_bytes)
    hex_hash = in_bytes.hex()
    n = int.from_bytes(input.read(4), "big")
    ts = int.from_bytes(input.read(4), "big")
    #out.write
    print(f"{n:10d}  {ts:10d}  {repr(bits[:28]):35s} {hex_hash:70s}")
    bits.clear()
    
input.close()
