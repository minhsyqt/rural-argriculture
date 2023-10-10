import socket
import time
from _thread import *
import threading
import argparse
import json

HOST = "localhost"
NUM_PORTS = 1000

def client_handler(connection, address):
    while True:
        try:
            # Receive data from client
            payload = json.loads(connection.recv(2048).decode("utf-8"))
            if not payload:
                break  # Break the loop if no data is received

            # Acknowledge message received
            print("{}:{} wrote: {}".format(address[0], address[1], payload))

            # Send reply back to client
            connection.sendall(json.dumps(payload).encode("utf-8"))
        except Exception as e:
            print(str(e))
            break

    connection.close()

def accept_connections(ServerSocket):
        client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        worker = threading.Thread(target=client_handler, args=(client, address))
        worker.start()

if __name__ == '__main__':
    start = time.time()

    # Create sockets for all ports
    sockets = []
    for PORT in range(1024, 1024 + NUM_PORTS):
        # Create a socket and bind to a port. SO_REUSEADDR=1 for reusing address
        ServerSocket = socket.socket()
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            ServerSocket.bind((HOST, PORT))
            sockets.append(ServerSocket)
        except socket.error as e:
            print(str(e))

    # Listen for connections on all sockets
    for ServerSocket in sockets:
        ServerSocket.listen()
        print('Server is listening on the port {}'.format(ServerSocket.getsockname()[1]))
        accept_connections(ServerSocket)
