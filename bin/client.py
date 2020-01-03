#!/usr/bin/env python3
import socket
import threading
import os, time
import tsock
import sys
import getopt
##################
"""
./client.py -s /etc/hosts -d True

"""
##################
DEFAULT_HOST='127.0.0.1'
DEFAULT_PORT=12345
if len(sys.argv)==2:
    HOST=sys.argv[1]
    PORT=sys.argv[2]
else:
    HOST=DEFAULT_HOST
    PORT=DEFAULT_PORT
    print("Contacting the default port {} and IP {}".format(PORT,HOST))

def main():
    print("Now parsing teh arguments")
##################
    print('ARGV      :', sys.argv[1:])
    options, remainder = getopt.gnu_getopt(
    sys.argv[1:], 's:d:v', ['source=', 'debug',])
    print('OPTIONS   :', options)
    debug=False
    saveset='/etc/hosts'
    for opt, arg in options:
        if opt in ('-s', '--saveset'):
            print('Saveset --saveset')
            saveset = arg
        elif opt in ('-d', '--debug'):
            print('Setting --debug.')
            debug = True

    print('DEBUG   :', debug)
    print('SAVESET    :', saveset)

##################
    s=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    sbuf=tsock.tsock(s)
    #files = input('Enter file(s) to send:')
    #files=os.listdir('originals')
    #files_to_send = files.split()
    files_to_send = [saveset ]
    for file in files_to_send:
        print("saving file", file)
        sbuf.put_header()
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
        print('File  Sent " ',file_name)
    print("going to sleep")
    time.sleep(3)
if __name__ == "__main__":main()
