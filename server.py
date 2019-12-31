#!/usr/bin/env python3
import socket
import threading
import os, signal
import tsock
import sys

DEFAULT_HOST='0.0.0.0'
DEFAULT_PORT=12345
if len(sys.argv)==2:
    HOST=sys.argv[1]
    PORT=sys.argv[2]
else:
    HOST=DEFAULT_HOST
    PORT=DEFAULT_PORT
    print("Using the default port {} and IP {}".format(PORT,HOST))
#PORT=int(PORT)

s=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
def main():
    #s=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    signal.signal(signal.SIGINT, receiveSignal)
    # If server and client run in same local directory,
    # need a separate place to store the uploads.
    try:
        os.mkdir('uploads')
    except FileExistsError:
        pass

    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(10)
    print("Waiting for a connection.....")
    while True:
       conn, addr = s.accept()
       print("I have received a connection from",addr )
       connbuf=tsock.tsock(conn)
       while True:
           header=connbuf.get_bytes(connbuf.HSIZE)
           header=header.decode("utf-8").strip()
           print("Packet type is:", header)
           bfilesize=connbuf.get_bytes(16)
           if not bfilesize:
               break
           filesize=int.from_bytes(bfilesize,'big')
           print("file size is",filesize)
           filename=connbuf.get_bytes(32)
           filename=filename.decode("utf-8").strip()
           print("file name  is",filename)
           filename = os.path.join('uploads',filename)
           with open(filename, 'wb') as f:
              chunk_size = 8 
              remaining = filesize
              while remaining:
                 chunk_size =4096 if remaining>=4096 else remaining
                 chunk = connbuf.get_bytes(chunk_size)
                 if not chunk: break
                 f.write(chunk)
                 #print("for testing only chunk_size is ",chunk_size)
                 #print("for testing only len(chunk) is ",len(chunk))
                 remaining -=chunk_size
              print('done for this file')
       print('done with this client he doesnt have more files')
def receiveSignal(signalNumber, frame):
    print('Received:', signalNumber)
    cleanup(s)
    return

def cleanup(s):
    #s.shutdown(socket.SHUT_RDWR)
    s.close()
    print("I have shutdown the socket")
    exit()
if __name__ == "__main__":main()

