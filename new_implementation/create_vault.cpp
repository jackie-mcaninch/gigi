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
    
    char hex_vals[256];
    //OPEN FILE FOR WRITING
    ofstream file1;
    file1.open("vault.bin", ios::out | ios::binary | ios::trunc);// | ios::app);
    //file2.open("vault2.bin", ios::out | ios::binary | ios::trunc);

    if (!file1) {
        cout << "Error opening file.\n";
        return 1;
    }

    //INIT VARIABLES
    int num_hashes;
    num_hashes = 4*32; //please use multiple of 32 for now
    string const_info = "wallet_addr+mac_addr";
    string temp_info;
    string complete_string;
    string hash;
    char buf[32*28];
    int nonce = 0;
    int buf_counter;

    
    //GENERATE HASHES AND DUMP TO DISK
    while (nonce<num_hashes) {
        buf_counter = nonce%32;
        temp_info = to_string(time(0)) + to_string(nonce);
        complete_string = const_info + temp_info;
        hash = sha224(complete_string);
        //cout << "\nrecord : " << hash;
        hex_to_bytes(hash.c_str(), &buf[buf_counter*28], hex_vals);
        nonce++;
        if (buf_counter==31) {
            file1.write(buf, 32*28);
        }
    }
    file1.close();
    return 0;
}