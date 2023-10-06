import socket
import time
from _thread import *
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default=None, help="Host IP address")
parser.add_argument("--port", type=int, default=9999, help="Port number")
args = parser.parse_args()


HOST = "localhost" if args.host is None else args.host
PORT = args.port

def client_handler(connection, address):
    while True:
        # Receive data from client
        payload = json.loads(connection.recv(2048).decode("utf-8"))
        # Acknowledge message received
        print("{}:{} wrote: {}".format(address[0], address[1], payload))

        # Send reply back to client
        connection.sendall(json.dumps(payload).encode("utf-8"))
    connection.close()

def accept_connections(ServerSocket):
    client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (client, address))


if __name__ == '__main__':
    start = time.time()

    # Create a socket and bind to a port. SO_REUSEADDR=1 for reusing address
    ServerSocket = socket.socket()
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        ServerSocket.bind((HOST, PORT))
    except socket.error as e:
        print(str(e))

    # Listen for connections
    ServerSocket.listen()
    print('Server is listening on the port {}'.format(PORT))

    # Accept connections forever
    while True:
        accept_connections(ServerSocket) 