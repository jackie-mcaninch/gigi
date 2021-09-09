#include <fstream>
#include <iostream>
#include <string>
#include <time.h>
#include "sha224.h"
using namespace std;

string hex_to_bytes(const string &hex_string) {
    string byte_string;
    char curr_byte;
    for (int i=0; i<32; i+=2) {
        curr_byte = (char) strtol(hex_string.substr(i,2).c_str(), NULL, 16);
        byte_string.push_back(curr_byte);
    }
    return byte_string;
}

int main(int argc, char *argv[]) {
    //OPEN FILE FOR WRITING
    ofstream file1("vault.bin", ios::out | ios::binary | ios::app);
    if (!file1) {
        cout << "Error opening file.\n";
        return 1;
    }

    //INIT VARIABLES
    int num_hashes;
    num_hashes = 128; //please use multiple of 32 for now
    string const_info = "wallet_addr+mac_addr";
    string temp_info;
    string complete_string;
    string hash;
    string buf[32];
    int nonce = 0;
    int buf_counter;

    //GENERATE HASHES AND DUMP TO DISK (BUF = 32*32 BYTES)
    while (nonce<num_hashes) {
        buf_counter = nonce%32;
        //cout << "buf_counter: " << buf_counter << "\n";
        temp_info = to_string(time(0)) + to_string(nonce);
        complete_string = const_info + temp_info;
        hash = sha224(complete_string);
        cout << "record : " << hash << "\n";
        if (buf_counter==31) {
            file1.write((char *) &buf, 1024);
        }
        //cout << "fp : " << file1.tellp() << "\n";
        buf[buf_counter] = hex_to_bytes(hash).c_str();
        nonce++;
    }
    
    return 0;
}