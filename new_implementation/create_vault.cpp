#include <fstream>
#include <iostream>
#include <string>
#include <string.h>
#include <time.h>
#include "sha224.h"
using namespace std;

const int RECS_PER_BLOCK = 32;

struct record {
    char hash[24];  //24-byte hash
    int n;          //4-byte nonce
    int ts;         //4-byte timestamp
};

void hex_to_bytes(const char* hex_string, char* out_byte_string, const char* hex_vals) {
    char curr_byte;
    for (int i=0, j=0; i<48; i+=2, j++) {
        curr_byte = hex_vals[(int)hex_string[i]]*16+hex_vals[(int)hex_string[i+1]];
        out_byte_string[j] = curr_byte;
    }
}

int main(int argc, char *argv[]) {
    //OPEN FILE FOR WRITING
    ofstream file1;
    file1.open("vault.bin", ios::out | ios::binary | ios::trunc);// | ios::app);

    if (!file1) {
        cout << "Error opening file.\n";
        return 1;
    }

    //INIT CONSTANT HEX VALUE REPRESENTATION
    char hex_vals[102];
    for (int i=0; i<102; i++) {
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

    //INIT VARIABLES
    string const_info = "wallet_addr+mac_addr";
    string temp_info;
    string complete_string;
    string hash;

    int num_hashes= atoi(argv[1]); //please use multiple of 32 for now
    int nonce = 0;
    int timestamp = time(0);

    record record_buf[RECS_PER_BLOCK*sizeof(record)];
    record* curr_record = &record_buf[0];
    int buf_counter;


    //GENERATE HASHES AND DUMP TO DISK
    clock_t s = clock();
    while (nonce<num_hashes) {
        buf_counter = nonce%RECS_PER_BLOCK;
        timestamp = time(0);
        temp_info = to_string(timestamp) + to_string(nonce);
        complete_string = const_info + temp_info;
        hash = sha224(complete_string);
        //cout << "record : " << hash << "\n";
        //cout << "curr_record address: " << curr_record << "\n";
        hex_to_bytes(hash.c_str(), &(curr_record->hash[0]), hex_vals);//&buf[buf_counter*24], hex_vals);
        curr_record->n = nonce;
        curr_record->ts = timestamp;
        nonce++;
        if (buf_counter==RECS_PER_BLOCK-1) {
            //NOTE: WRITES NONCE AND TIMESTAMP WITH LITTLE ENDIANNESS
            file1.write((const char*)&record_buf, 32*sizeof(record));
            //timestamp = time(0);
            curr_record -= RECS_PER_BLOCK;
        }
        curr_record++;
    }
    file1.write((const char*)&record_buf, (buf_counter+1)*sizeof(record));  //flush remnants inside buffer
    clock_t e = clock();

    //FINISH
    cout << "TIME FOR GENERATION AND DUMP: " <<  ((double)(e-s)/CLOCKS_PER_SEC) << "\n";
    file1.close();
    return 0;
}