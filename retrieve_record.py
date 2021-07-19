#establish target... from args? or file?
#comb through filter file
#mark every file that is flagged
#find starting point (uniform distribution)
#perform binary search
#write vault message

import sys
import os

diff = 4
challenge = bytes.fromhex(sys.argv[1]) #input should be in hex format
key = challenge[:diff]
loc_index = int.from_bytes(challenge[:4], "big")/4294967295
file_size = os.stat("vaults/testing.bin").st_size
start_pt = int(loc_index*(file_size - 270))
print(start_pt)

file_name = "vaults/testing.bin"
seeker = open(file_name, "r")