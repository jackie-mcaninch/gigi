#include <fstream>
#include <iostream>
#include <string>
#include <string.h>
#include <time.h>
#include <math.h>
#include "sha224.h"
using namespace std;

struct record {
    char hash[24];  //24-byte hash
    int n;          //4-byte nonce
    int ts;         //4-byte timestamp
};

void hex_to_bytes(const char *hex_string, char *out_byte_string, const char *hex_vals) {
    char curr_byte;
    for (int i=0, j=0; i<48; i+=2, j++) {
        curr_byte = hex_vals[(int)hex_string[i]]*16+hex_vals[(int)hex_string[i+1]];
        out_byte_string[j] = curr_byte;
    }
}

void bit_shift(char* key, const char* hash, int num_bits) {
    unsigned bits1 = (unsigned)key[0], bits2 = (unsigned)key[1];
    unsigned mask;
    unsigned overflow_bits;
    if (num_bits < 8) {
        mask = (1<<num_bits-8)-1;
    }
    else {
        mask = 0;
    }
    overflow_bits = bits1 & mask;
    bits1 >> num_bits;
    bits2 >> num_bits;
    bits2 = overflow_bits | bits2;
    key[0] = (char) bits1;
    cout << "key[0] assigned...    ";
    cout << key[0] <<"\n";
    key[1] = (char) bits2;
    cout << "key[1] assigned...    ";
    cout << key[1] <<"\n";
}

// execution: ./bucket_create <num_recs_in_vault> <records_per_block> <mem_available_in_bytes>
int main(int argc, char *argv[]) {

    // ASSIGN CONSTANT VALUES DEFINED IN ARGUMENTS
    const int NUM_RECS_IN_VAULT = atoi(argv[1]);                            // n
    const int VAULT_SIZE_IN_BYTES = 32*NUM_RECS_IN_VAULT;                   // N
    const int RECS_PER_BLOCK = atoi(argv[2]);                               // k
    const int BYTES_PER_BLOCK = 32*RECS_PER_BLOCK;                          // K
    const int MEM_AVAILABLE_IN_BYTES = atoi(argv[3]);                       // M
    const int MAX_RECS_IN_MEM = (int)(MEM_AVAILABLE_IN_BYTES/32);
    const int NUM_BUCKETS = (int)(MEM_AVAILABLE_IN_BYTES/BYTES_PER_BLOCK);  // x
    const int NUM_PRECEDING_BITS = (int)log2((double)NUM_BUCKETS);
    const int HEADER_SIZE = 1024;

    if (2*BYTES_PER_BLOCK > MEM_AVAILABLE_IN_BYTES) {
        cout << "MEMORY (ARG 3) MUST BE AT LEAST 64X THE NUMBER OF RECORDS PER BLOCK (ARG 2)\n";
        return -1;
    }
    // cout << "mem available in bytes " << MEM_AVAILABLE_IN_BYTES << "\n";
    // cout << "bytes per block " << BYTES_PER_BLOCK << "\n";
    // cout << "num buckets " << NUM_BUCKETS << "\n";
    // cout << "num preceding bits " << NUM_PRECEDING_BITS << "\n";

    // OPEN FILE FOR WRITING
    ofstream file1;
    file1.open("vault.bin", ios::out | ios::binary | ios::trunc);// | ios::app);

    if (!file1) {
        cout << "ERROR OPENING FILE!\n";
        return 1;
    }

    // INIT CONSTANT HEX VALUE REPRESENTATION
    char hex_vals[103];
    for (int i=0; i<103; i++) {
        hex_vals[i] = 0;
    }
    hex_vals['0'] = 0;
    hex_vals['1'] = 1;
    hex_vals['2'] = 2;
    hex_vals['3'] = 3;
    hex_vals['4'] = 4;
    hex_vals['5'] = 5;
    hex_vals['6'] = 6;
    hex_vals['7'] = 7;
    hex_vals['8'] = 8;
    hex_vals['9'] = 9;
    hex_vals['a'] = 10;
    hex_vals['b'] = 11;
    hex_vals['c'] = 12;
    hex_vals['d'] = 13;
    hex_vals['e'] = 14;
    hex_vals['f'] = 15;

    // INIT VARIABLES
    char const_info[HEADER_SIZE] = "0123456789abcdef0123456789abcdef9cb6d08f6a02";
    string temp_info;
    string complete_string;
    string hash;
    char *hash_bytes = (char *)malloc(sizeof(char)*24);
    char *hash_key = (char *)malloc(sizeof(char)*NUM_PRECEDING_BITS);

    int nonce = 0;
    int timestamp = time(0);

    record **records = (record **)malloc(MAX_RECS_IN_MEM*sizeof(record *));
    for (int i=0; i<MAX_RECS_IN_MEM; i++) {
        records[i] = (record *)malloc(sizeof(record));
    }
    if (*records==NULL) {
        cout << "ERROR ALLOCATING MEMORY!\n";
        return -1;
    }


    // PRINT HEADER TO FILE
    file1.write(const_info, HEADER_SIZE);

    // GENERATE HASHES AND DUMP TO DISK IN BUCKETS
    clock_t s = clock();
    while (nonce<NUM_RECS_IN_VAULT) {
        timestamp = time(0);
        temp_info = to_string(timestamp) + to_string(nonce);
        complete_string = const_info + temp_info;
        hash = sha224(complete_string);
        cout << hash << "\n" ;
        hex_to_bytes(hash.c_str(), hash_bytes, hex_vals);
        bit_shift(hash_key, hash.c_str(), 24-NUM_PRECEDING_BITS);
        cout << hash_key << "\n";
        nonce++;
        return 0;
        //put hash through funct to get bucket num
        //save bucket num
        //call hex_to_bytes on hash and place in bucket
        //assign nonce and timestamp to said record
        //if that bucket becomes full, flush bucket[bucket_num] to disk
        //implement later: add item to unordered hash map <int, std::list>
        
    }
    clock_t e = clock();

    // FINISH
    cout << "TIME FOR GENERATION AND DUMP: " <<  ((double)(e-s)/CLOCKS_PER_SEC) << "\n";
    file1.close();
    free(records);
    return 0;
}