import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("You have joined the Chat Room!", "utf8"))
        addresses[client] = client_address
        Thread(target=lambda a: handle_client(a,client_address), args=(client,)).start()


def handle_client(client,client_address):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    if name == "{quit}":
        client.close()
        print("%s:%s has disconnected." % client_address)
    else:
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
        print(list(clients.values()))
        while True:
            msg = client.recv(BUFSIZ)
            print(msg.decode("utf8"))
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name+": ")
            else:
                client.close()
                print("%s:%s has disconnected." % client_address)
                del clients[client]
                """if len(clients) == 0:
                                                        SERVER.close()
                                                        sys.exit(0)
                                                        break"""

                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = 'localhost'
PORT = 5431
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()