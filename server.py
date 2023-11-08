#need to reimplement to use mongoAPI
import socket
import time
from _thread import *
import threading
import argparse
import json
import selectors
import mongoAPI
import geoAPI
import requests

# Important Global Configurations
HOST = "localhost"
NUM_PORTS = 256

def handle_signup(connection, payload):
    # Send reply back to client
    connection.sendall(json.dumps("Signup sucessful!").encode("utf-8"))
    latitude  = payload["farm_location_lat"]
    longitude = payload["farm_location_long"]

    #Get more information from lat/long with OpenCage
    city, county, state, country = geoAPI.get_city_country(latitude, longitude)

    # Insert new entry into MongoDB
    new_user = {
        "phone_number": payload["phone_number"],
        "location": {
            "latitude": float(latitude),
            "longitude": float(longitude),
            "city": city,
            "county": county,
            "state": state,
            "country": country
        }
    }
    mongoAPI.createUser(new_user)


def handle_login(connection, payload):
    pass

def client_handler(connection, address):
    while True:
        try:
            # Receive data from client
            payload = json.loads(connection.recv(2048).decode("utf-8"))
            if not payload:
                break  # Break the loop if no data is received

            # Acknowledge message received
            # print("{}:{} wrote: {}".format(address[0], address[1], payload))

            if payload["request_type"] == "signup":
                handle_signup(connection, payload)
            elif payload["request_type"] == "login":
                handle_login(connection, payload)

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

    # Setup MongoDB
    mongoAPI.connect("World", "Farners")

    # Setup sockets
    start = time.time()
    sel = selectors.DefaultSelector()

    for PORT in range(1024, 1024 + NUM_PORTS):
        # Create a socket and bind to a port. SO_REUSEADDR=1 for reusing address
        ServerSocket = socket.socket()
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            ServerSocket.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
        ServerSocket.listen()
        ServerSocket.setblocking(False)
        sel.register(ServerSocket, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                accept_connections(key.fileobj)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()
        mongoAPI.disconnect()