import mmh3
from bitarray import bitarray
import os
import io
import time

class filter:
    def __init__(self):
        pass

    def add_filter(self, vault_file, diff):
        #init empty filter
        try: os.chdir("vaults")
        except: os.chdir("../vaults")
        filter_size = 83885824
        filter = bitarray("0"*filter_size, endian="big")

        #read input
        reader = open(vault_file, "rb")
        file_size = os.stat(vault_file).st_size
        reader.seek(46)
        record = bitarray(256, endian="big")
        # s = time.time()
        
        #place values into filter
        while reader.tell() < file_size:
            buf = reader.read((io.DEFAULT_BUFFER_SIZE//40)*40)
            i = 0
            while i < (len(buf)//40):
                #hash the records
                #number of records in full vault: 26,843,544
                #number of slots for any filter: 83,885,824
                #number of different hash functions: 2
                record.clear()
                record.frombytes(buf[i*40:(i*40)+32])
                digest1 = mmh3.hash(record[:diff].tobytes(), 1) % filter_size
                digest2 = mmh3.hash(record[:diff].tobytes(), 2) % filter_size
                filter[digest1] = True
                filter[digest2] = True
                i += 1
        reader.close()
        # e = time.time()
        # print(f"TOTAL TIME TAKEN: {e-s:.4f}")

        #open filter files and write
        curr = open("current-filter-"+str(diff)+".bin", "wb")
        curr.write(filter.tobytes())
        curr.close()

    def eval_filters(self):
        pass
        #possible function to re-evaluate vault filters after a difficulty change (supports multiple vaults)        

    def clean_filters(self, diff):
        for _, _, files in os.walk(os.getcwd()):
            for file in files:
                if file[:15]=="current-filter-" and file[15:]!=str(diff)+".bin":
                    os.remove(file)
            

