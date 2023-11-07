import socket
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default=None, help="Host IP address")
parser.add_argument("--port", type=int, default=1024, help="Port number")
args = parser.parse_args()


HOST = "localhost" if args.host is None else args.host
PORT = args.port

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server 
    try:
        sock.connect((HOST, PORT))
        print("Connected to server")
    except socket.error as e:
        print(str(e))

    # Continuously ask for data to be sent to the server
    while True:

        inp = input("Enter message: ")
        # TODO: fix exit command
        # if inp == "exit":
        #     break

        try:
            # Send data
            sock.send(json.dumps(inp).encode("utf-8"))
            # Receive data from the server
            received = json.loads(sock.recv(1024).decode("utf-8"))
            print("Received: {}".format(received))
        except socket.error as e:
            print(str(e))
            print("Server is down")
            break
print("Connection closed.")