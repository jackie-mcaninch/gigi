import numpy as np
import mmh3
from bitarray import bitarray

class Bloom:
    def __init__(self, size, diff):
        print("creating bloom filter...")
        self.size = size
        self.barray = bitarray(size)
        self.barray.setall(0)
        self.difficulty = int(diff)
    
    def __repr__(self):
        s = ""
        for b in self.barray:
            s+=str(b)
        return s

    def insert(self, item):
        arr = bytearray(item)
        trimmed_item = arr[0:self.difficulty]
        self.barray[self.my_hash(trimmed_item)]=True

    def my_hash(self, item):
        result = mmh3.hash(str(item))
        return result % self.size

    def lookup(self, item):
        arr = bytearray(item)
        trimmed_item = arr[:self.difficulty]
        return self.barray[self.my_hash(trimmed_item)]

    def get_bytes(self):
        return bytes(self.barray)
    
def calc_filter_size(num_records, prob):
    m = int((num_records*-1)/0.48045)*np.log(prob)
    if m > 1000000:
        m = int((m//1000000)*1000000)
    return m

def init_filter_file(diff):
    a = open("filters.txt","wb")
    a.write(diff.to_bytes(32, "big"))
    a.close()