#!/usr/bin/env python3
import socket
import threading
import os
import tsock
import sys

DEFAULT_HOST='127.0.0.1'
DEFAULT_PORT=12345
def main(HOST=DEFAULT_HOST,PORT=DEFAULT_PORT):
    s=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    sbuf=tsock.tsock(s)
    #files = input('Enter file(s) to send:')
    files=os.listdir('originals')
    #files_to_send = files.split()
    files_to_send = files
    for file in files_to_send:
        file_name=os.path.join('originals',file)
        print("The file to be sent is:", file_name)
        file_size = os.path.getsize(file_name)
        print("The file size is :",file_size)
        padded_fname="{:<32}".format(file_name)
        binary_file_name=str.encode(padded_fname)
        print("The file name is encoded to binary:",binary_file_name)
        sbuf.put_bytes(file_size.to_bytes(16,'big'))
        sbuf.put_bytes(binary_file_name)
        with open(file_name, 'rb') as f:
              sbuf.put_bytes(f.read())
        print('File Sent " ',file_name)
if __name__ == "__main__":main(sys.argv[1],int(sys.argv[2]))
