#!/usr/bin/env python3
import socket
import sys
import time
import threading

# IP to listen on
SERVER_IP = '0.0.0.0' 

# Port to listen on
SERVER_PORT = int(sys.argv[1])

# MAXCLIENTS defined the max server allowed connecions
MAX_CLIENT=100

GREETING_MESSAGE="Welcome to the server !!!".encode('utf-8')
list_of_clients = [] 

def Server(IP,port):
    """
    Here we create the server listening socket
    :return:
    """
    print("Starting the server socket !!! ",IP," and port ", port)
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, socket.SO_REUSEPORT)
    """ 
    binds the server to an entered IP address and at the 
    specified port number. 
    Th e client must be aware of these parameters 
    """
    server.bind((IP, port))
    server.listen(MAX_CLIENT)
    while True:
      client_connection, client_addr= server.accept()
      list_of_clients.append(client_connection)
      print("I Got connection from ", client_addr[0]) 
      threading.Thread(target=client_thread,args=(client_connection,client_addr)).start()
    # Close the opened sockets
    client_connection.close()
    server.bind.close()
"""
client_thread will handle the client connection

"""
def client_thread(conn, addr):
    # send welcome message
    #conn.sendall(GREETING_MESSAGE)
    #conn.sendall("Hello Again".encode('utf-8'))
    while True:
        byte_message = conn.recv(20480)
        if byte_message:
           message=byte_message.decode('utf-8')
           print ("<", addr[0], "> ", message)
           message_to_send = "<" + addr[0] + "> " + message 
           byte_message_to_send=message_to_send.encode('utf-8')
           broadcast(byte_message_to_send, conn) 
        else: 
           """message may have no content if the connection 
           io s broken, in this case we remove the connection"""
           print("failed")
           #remove(conn) 

"""
send to all sockets what we receive

"""
def broadcast(message, connection):
    #print(list_of_clients)
    for clients in list_of_clients: 
        try: 
            clients.sendall(message) 
        except: 
            clients.close() 
            # if the link is broken, we remove the client 
            #remove(clients) 

def main():
    Server(SERVER_IP,SERVER_PORT)
if __name__ == '__main__': main()
