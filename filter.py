import mmh3
from bitarray import bitarray
import os
import io
import time

class filter:
    def __init__(self):
        print("new filter created")

    def new_vault(self, vault_file, diff):
        #init empty filters
        try: os.chdir("vaults")
        except: os.chdir("../vaults")
        filter = bitarray("0"*83885824)
        if diff > 1:
            safety_lo =  bitarray("0"*83885824)
        if diff < 256:
            safety_hi =  bitarray("0"*83885824)

        #read input
        reader = open(vault_file, "rb")
        file_size = os.stat(vault_file).st_size
        reader.seek(46)
        record = bitarray(256)
        s = time.time()
        while reader.tell() < file_size:
            buf = reader.read((io.DEFAULT_BUFFER_SIZE//40)*40)
            i = 0
            while i < len(buf):
                #hash the records
                #number of records in vault: 26,843,544
                #number of slots in every filter: 83,885,824
                #number of different hash functions: 2
                record.frombytes(buf[i*40:(i*40)+32])
                digest1 = mmh3.hash(record[:diff].tobytes(), 1) % 83885824
                digest2 = mmh3.hash(record[:diff].tobytes(), 2) % 83885824
                filter[digest1] = True
                filter[digest2] = True
                if diff > 1:
                    digest1 = mmh3.hash(record[:diff-1].tobytes(), 1) % 83885824
                    digest2 = mmh3.hash(record[:diff-1].tobytes(), 2) % 83885824
                    safety_lo[digest1] = True
                    safety_lo[digest2] = True
                if diff > 1:
                    digest1 = mmh3.hash(record[:diff+1].tobytes(), 1) % 83885824
                    digest2 = mmh3.hash(record[:diff+1].tobytes(), 2) % 83885824
                    safety_hi[digest1] = True
                    safety_hi[digest2] = True
                i += 40
        
        reader.close()
        os.chdir("..")
        e = time.time()
        print(f"TOTAL TIME TAKEN: {e-s:.4f}")

        #move to / create filter directory
        try:
            os.chdir("filters")
        except:
            os.mkdir("filters")
            os.chdir("filters")

        #open filter files and write
        curr = open("current-filter-"+str(diff)+".bin", "ab")
        curr.write(bytes(vault_file, "utf-8"))
        curr.write(filter.tobytes())
        curr.close()
        
        if diff > 1:
            print("opening low safety file named", "safety-filter-"+str(diff-1)+".bin")
            s_lo = open("safety-filter-"+str(diff-1)+".bin","ab")
            s_lo.write(bytes(vault_file, "utf-8"))
            s_lo.write(safety_lo.tobytes())
            s_lo.close()

        if diff < 256:
            print("opening high safety file")
            s_hi = open("safety-filter-"+str(diff+1)+".bin","ab")
            s_hi.write(bytes(vault_file, "utf-8"))
            s_hi.write(safety_hi.tobytes())
            s_hi.close()


    def eval_vaults(self, diff):
        os.chdir("filters")
        for root, _, files in os.walk("filters"):
            for file in files:
                if file[14:] == str(diff)+".bin":
                    os.rename(file, "current-filter-"+str(diff))
                else:
                    print("removing",os.path.join(root,file))
                    os.remove(os.path.join(root, file))

        os.chdir("..")
        if diff > 1:
            for _, _, files in os.walk("vaults"):
                for file in files:
                    if file != "testing.bin":
                        self.new_vault(file, diff-1)
        if diff < 256:
            for _, _, files in os.walk("vaults"):
                for file in files:
                    if file != "testing.bin":
                        self.new_vault(file, diff+1)
        

    def clean_filters(self):
        pass
        #possible function to clear unused filters from file (in the case of deleted vaults)
            

