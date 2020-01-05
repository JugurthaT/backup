#!/usr/bin/env python3
import socket
import threading
import os, signal
import tsock
import sys

#HEADER=b'Transfer'
HSIZE=32
STOP_JOB = 'STOP_JOB'
FOLDER_JOB='MKDIR_FOLDER'
LINK_JOB='MK_LINK'
FILE_JOB='BKP_FILE'
class tsock:
    def __init__(self,s):
        self.sock= s
        self.buffer = b''
        #self.HEADER=b'TransferFiles'
        #self.HSIZE=len(self.HEADER)

    def put_bytes(self,data):
        self.sock.sendall(data)

    def get_bytes(self,n):
        '''Read exactly n bytes from the buffered socket.
           Return remaining buffer if <n bytes remain and socket closes.
        '''
        data = self.sock.recv(n)
        return data 
    def put_header(self,header):
        padded_header="{:<32}".format(header) 
        #print("put_header : padded_header=",padded_header)
        self.sock.sendall(str.encode(padded_header)) 

    def get_header(self):
        data = self.sock.recv(32)
        unpad_data=data.decode("utf-8").strip()
        return unpad_data
    def send_stop(self):
        self.sock.sendall(str.encode('STOP_JOB'))
