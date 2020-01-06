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
'''if len(sys.argv)==2:
    HOST=sys.argv[1]
    PORT=sys.argv[2]
else:
'''
HOST=DEFAULT_HOST
PORT=DEFAULT_PORT
print("Contacting the default port {} and IP {}".format(PORT,HOST))

def main():
    print("Now parsing the arguments")
##################
    #print('ARGV      :', sys.argv[1:])
    options, remainder = getopt.gnu_getopt(
    sys.argv[1:], 's:d:f:l:v', ['source=', 'debug',])
    #print('OPTIONS   :', options)
    debug=False
    saveset="/etc/hosts"
    for opt, arg in options:
        if opt in ('-s', '--saveset'):
            #print('Saveset --saveset')
            saveset = arg
            print("Saveset list is: ",saveset)
            JTYPE='FILE_JOB'
        elif opt in ('-d', '--debug'):
            print('Setting --debug.')
            debug = True
        elif opt in ('-f', '--folder'):
            print('creating a folder --folder.')
            header='MKDIR_FOLDER' 
            saveset = arg
            print("Saveset list is: ",saveset)
            JTYPE='FOLDER_JOB'

    print('DEBUG   :', debug)
    print('SAVESET    :', saveset)

    '''
    we connect to server and send the data
    '''
    s=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    sbuf=tsock.tsock(s)
    files_to_send = [saveset ]
    for f in files_to_send:
       send_item(f,sbuf) 
    print("going to sleep")
    sbuf.send_stop()
    s.close()
    #time.sleep(3)

#################################################
def send_item(item,buf):
    if os.path.islink(item):
        return
    if os.path.isfile(item):
        send_a_file(item,buf)
    elif os.path.isdir(item):
        send_a_folder(item,buf)
        print("send_item: Now we check te folders under",item)
        sub_set=listdir_fullpath(item)
        #print("send_item: Now we check ",sub_set)
        for sub_item in sub_set:
            #okk=input("next ?")
            f_sub_set=os.path.join(item,sub_item) 
            print("send_item: Now we send :",f_sub_set)
            send_item(sub_item,buf)

def send_a_folder(fldrname,sbuf):
    print("saving :", fldrname)
    header=tsock.FOLDER_JOB
    padded_header="{:<512}".format(header)
    print("send padd_header",padded_header, "length is",len(padded_header))
    sbuf.put_bytes(str.encode(padded_header))
    padded_fldrname="{:<512}".format(fldrname)
    print("send padd_fldrname: ",padded_fldrname,"length is",len(padded_fldrname))
    sbuf.put_bytes(str.encode(padded_fldrname))

def send_a_file(fname,sbuf):
    print("saving :", fname)
    header=tsock.FILE_JOB
    print("header is :", header)
    sbuf.put_header(header)
    file_name=fname
    print("The file to be sent is:", file_name)
    file_size = os.path.getsize(file_name)
    print("The file size is :",file_size)
    padded_fname="{:<512}".format(file_name)
    binary_file_name=str.encode(padded_fname)
    print("The file name is :",fname)
    sbuf.put_bytes(file_size.to_bytes(16,'big'))
    sbuf.put_bytes(binary_file_name)
    with open(file_name, 'rb') as f:
        sbuf.put_bytes(f.read())
    print('File  Sent " ',file_name)

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

if __name__ == "__main__":main()

