make: create_vault.cpp sha224.cpp
	g++ -Wall create_vault.cpp sha224.cpp -o create

test: create_vault.cpp sha224.cpp
	g++ -Wall create_vault.cpp sha224.cpp -o create
	./create

test_out_py: create_vault.cpp sha224.cpp
	g++ -Wall create_vault.cpp sha224.cpp -o create
	./create
	python3 read_bin.py 128