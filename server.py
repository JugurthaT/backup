import socket
import sys



# IP to listen on
IP_address = str("0.0.0.0") 

# Port to listen on
Port = int(1234)

def Server():
    """
    Here we create the server listening socket
    :return:
    """
    print("Starting the server socket !!!")
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, socket.SO_REUSEPORT)
    if len(sys.argv) !=3:
        print("Missing arguments")
        exit()
    """ 
    binds the server to an entered IP address and at the 
    specified port number. 
    Th e client must be aware of these parameters 
    """
    server.bind((IP_address, Port))

if __name__ == '__main__': Server()
