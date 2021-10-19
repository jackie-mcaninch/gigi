#!/bin/bash

#make
#./create 1000000
#./create 5000000
#./create 10000000
#./create 15000000
#./create 20000000
#./create 33554432
time parallel -j 8 --bar -k ./create 211392922 /data/temp/vault8.bin {1} >> results8.txt ::: 1 2 3 4 5 6 7 8
time parallel -j 4 --bar -k ./create 211392922 /data/temp/vault4.bin {1} >> results4.txt ::: 1 2 3 4
time parallel -j 2 --bar -k ./create 211392922 /data/temp/vault2.bin {1} >> results2.txt ::: 1 2
time ./create 187904819 /data/temp/vault1.bin >> results1.txt
