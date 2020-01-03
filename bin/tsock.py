#!/usr/bin/env python3
import socket
import threading
import os, signal
import tsock
import sys

#HEADER=b'Transfer'
#HSIZE=len(HEADER)
class tsock:
    def __init__(self,s):
        self.sock= s
        self.buffer = b''
        self.HEADER=b'TransferFiles'
        self.HSIZE=len(self.HEADER)
    def get_header(self,n):
        '''Read exactly n bytes from the buffered socket.
           Return remaining buffer if <n bytes remain and socket closes.
        '''
        data = self.sock.recv(8)
        print("I received",data)            

    def put_bytes(self,data):
        self.sock.sendall(data)

    def get_bytes(self,n):
        '''Read exactly n bytes from the buffered socket.
           Return remaining buffer if <n bytes remain and socket closes.
        '''
        data = self.sock.recv(n)
        return data 
    def put_header(self):
        self.sock.sendall(self.HEADER) 
    def get_header(self):
        data = self.sock.recv(self.HSIZE)
        return data
