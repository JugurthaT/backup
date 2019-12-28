import socket
import sys


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


if __name__ == '__main__': Server()
