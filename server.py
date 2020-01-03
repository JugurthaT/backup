#!/usr/bin/env python3
import socket
import threading
import os, signal
import tsock, catalog 
import sys
"""
./server.py 
"""
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
       ## Create job id and folder
       newjob=catalog.job()
       JOBID=str(newjob.get_jobid())
       print("the new jobs id is",JOBID)
       connbuf=tsock.tsock(conn)
       ## call conne_handler(connbuf)
       connection_handler(connbuf,JOBID,newjob)
       print('done with this client he doesnt have more files')
       
def connection_handler(conn,JOBID,j):
    while True:
        header=conn.get_bytes(conn.HSIZE)
        header=header.decode("utf-8").strip()
        print("Packet type is:", header)
        bfilesize=conn.get_bytes(16)
        if not bfilesize:
           break
        filesize=int.from_bytes(bfilesize,'big')
        print("file size is",filesize)
        filename=conn.get_bytes(32)
        filename=filename.decode("utf-8").strip()
        sfilename=filename
        if filename.startswith('/'):
             filename=filename[1:]
        print("file name  is",filename)
        basepath='uploads'
        FullPath = os.path.join(basepath,filename)
        F_SAVE=relative_path(j,JOBID,filename)
        #FileSave=FullPath.split("/")[-1]
        #print("the saved file in destination is: ",FileSave)
        with open(F_SAVE, 'wb') as f:
           chunk_size = 8
           remaining = filesize
           while remaining:
              chunk_size =4096 if remaining>=4096 else remaining
              chunk = conn.get_bytes(chunk_size)
              if not chunk: break
              f.write(chunk)
              #print("for testing only chunk_size is ",chunk_size)
              #print("for testing only len(chunk) is ",len(chunk))
              remaining -=chunk_size
        insert_in_catalog(j,JOBID,sfilename,F_SAVE)
        print('done for this file')
       #print('done with this client he doesnt have more files')
def insert_in_catalog(job,jobid,sfilename,filename):
    job.update_catalog(jobid,sfilename,filename)

def receiveSignal(signalNumber, frame):
    print('Received:', signalNumber)
    cleanup(s)
    return

def cleanup(s):
    #s.shutdown(socket.SHUT_RDWR)
    s.close()
    print("I have shutdown the socket")
    exit()

def relative_path(j,jobid,filename):

    parent_dir=os.path.split(filename)[0]
    FileSave=os.path.split(filename)[1]
    J_PATH=j.get_base_path()
    P_dir=os.path.join(J_PATH,jobid,parent_dir)
    os.makedirs(P_dir,exist_ok=True)
    D_File=os.path.join(P_dir,FileSave)
    print("the dest file is:",D_File)
    return D_File

if __name__ == "__main__":main()

