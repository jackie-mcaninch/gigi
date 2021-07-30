# Green Lightning Coin - Vault

This repo handles the calculation, storage, and retrieval of hash records used to compare against current blockchain hashes and ultimately decide the winners/validators of every block.

## File Descriptions

**create_vault.py**: The main function for creating the vaults. Handles hash generation, record sorting, writing to disk, and building bloom filters. Meant to be run by any node that wishes to mine and validate gigi blocks.

**filter.py**: File for describing the filter class, meant to be called by create_vault.py. Holds functions for constructing bloom filter from a given vault, clearing all filters currently not in use, and re-evaluating vault filters after a difficulty change (soon to be implemented).

**gen_rand_chal.py**: Helper script to generate a string representation of a random 256-bit value. Outputs this string to random_challenge.txt which can then be copied and pasted into command line for testing vault.py.

**read_bin.py**: Another helper script that reads a binary vault file and converts it to human-readable format. Output is stored in records.txt and contains header information followed by records displayed in row format consisting of nonce, timestamp, string representation of hash, and hex representation of hash.

**retrieve_record.py**: Function for retrieving a record in a vault given a certain difficulty and target hash string. NO LONGER IN USE: SEE NODE/VAULT.PY INSTEAD.

**node/vault.py**: The main function for retrieving a matching hash record, through filter consultation and efficient disk search. 

*All other files are from the **node** repo and are not relevant toward the vault segment of the project.*

## Usage

Files should be run from the command line using the following syntax:

* python create_vault.py `<num_records>`
  * `<num_records>` is an optional argument to specify how many records will exist in the vault. Default is 26,843,544 (equals 1GiB) and any other value should be used for testing only.
 
* python gen_rand_chal.py
  * no additional arguments are necessary. Used for testing only.
 
* python read_bin.py `<num_print>`
  * `<num_print>` specifies how many records will be shown. Ex: read_bin.py 20 will print the first 20 records found in the file.
  
* python vault.py find `<hash>` `<difficulty>` `<block_size>`
  * `<hash>` is a string representation of the target hash.
  * `<difficulty>` is an int describing how many bits will be used to determine a match (filters only work for difficulty = 25).
  * `<block_size>` is an optional argument to specify the size in bytes of memory chunk loaded at a time to search for the target hash. Default is 4,000 bytes.
  
## Dependencies

The following modules must be installed to terminal before running the above files:
* hashlib
* uuid
* numpy
* mmh3
* bitarray
* kafka-python
