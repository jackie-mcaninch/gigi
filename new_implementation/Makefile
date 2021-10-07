make: create_vault.cpp sha224.cpp
	g++ -Wall -O3 create_vault.cpp sha224.cpp -o create

test: create_vault.cpp sha224.cpp
	g++ -Wall -O3 create_vault.cpp sha224.cpp -o create
	./create 128

test_out_py: create_vault.cpp sha224.cpp
	g++ -Wall -O3 create_vault.cpp sha224.cpp -o create
	./create 128
	python3 read_bin.py 128

comp_hex: create_vault.cpp sha224.cpp
	g++ -Wall -O3 create_vault.cpp sha224.cpp -o create
	./create 128
	hexdump -C vault.bin
	python3 read_bin.py 128

time: create_vault.cpp sha224.cpp
	g++ -Wall -O3 create_vault.cpp sha224.cpp -o create
	time ./create 128