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

#PRINT INDIVIDUAL RECORDS (SORTED BY HASH VALUE)
for i in range(16):
    n = int.from_bytes(input.read(4), "big")
    ts = int.from_bytes(input.read(4), "big")
    hash = input.read(32).hex()
    print(f"{n:2d}  {ts:d}  {hash:s}")

input.close()
