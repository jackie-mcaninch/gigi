#include <fstream>
#include <iostream>
#include <string>
#include <time.h>
#include "sha224.h"
using namespace std;

void hex_to_bytes(const char* hex_string, char* out_byte_string, const char* hex_vals) {
    char curr_byte;
    for (int i=0, j=0; i<56; i+=2, j++) {
        curr_byte = hex_vals[hex_string[i]]*16+hex_vals[hex_string[i+1]];
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

    //INIT VARIABLES
    string const_info = "wallet_addr+mac_addr";
    string temp_info;
    string complete_string;
    string hash;

    int num_hashes= 4*32; //please use multiple of 32 for now
    int nonce = 0;
    int buf_counter;
    
    char hex_vals[256];
    char buf[32*28];
    
    //INIT CONSTANT HEX VALUE REPRESENTATION
    for (int i=0; i<256; i++) {
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
    
    //GENERATE HASHES AND DUMP TO DISK
    while (nonce<num_hashes) {
        buf_counter = nonce%32;
        temp_info = to_string(time(0)) + to_string(nonce);
        complete_string = const_info + temp_info;
        hash = sha224(complete_string);
        cout << "record : " << hash << "\n";
        hex_to_bytes(hash.c_str(), &buf[buf_counter*28], hex_vals);
        nonce++;
        if (buf_counter==31) {
            file1.write(buf, 32*28);
        }
    }
    file1.close();
    return 0;
}