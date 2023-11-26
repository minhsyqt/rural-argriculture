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
NUM_PORTS = 2048

def handle_signup(connection, payload):
    # Setup MongoDB
    mongoAPI.connect("World", "Farmers")
    # Send reply back to client
    connection.sendall(json.dumps("Signup sucessful!").encode("utf-8"))
    latitude  = payload["farm_location_lat"]
    longitude = payload["farm_location_long"]

    city = "n/a"
    county = "n/a"
    country = "n/a"
    state = "n/a"

    #Get more information from lat/long with OpenCage (uncomment to use the service)
    #city, county, state, country = geoAPI.get_city_country(latitude, longitude)

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

def handle_send_image(connection, phone_number, image_data):
    # Setup MongoDB
    mongoAPI.connect("World", "Plant_Images")
    # Send reply back to client
    connection.sendall(json.dumps("Send image successful!").encode("utf-8"))

    new_entry = {"phone_number": phone_number, "image_data": image_data, "done": "false"}

    # Insert new entry into MongoDB
    mongoAPI.createImageEntry(new_entry)

def client_handler(connection, address):
    try:
        image_data = []  # Initialize an empty bytes object
        leftover = ""

        while True:
            # Receive data from client
            raw = connection.recv(4096).decode("utf-8")

            payload_list = raw.split("\n")

            for payload in payload_list:
                if "{" not in payload:
                    payload = leftover + payload
                    leftover = ""
                if "}" not in payload:
                    leftover = payload
                    continue

                payload = json.loads(payload)
                if payload["request_type"] == "signup":
                    handle_signup(connection, payload)
                    return
                elif payload["request_type"] == "send_image":
                    # Collect image data chunks
                    image_data += payload["chunk_data"]
                    if payload["chunk_index"] == payload["total_chunks"] - 1:
                        # Last chunk received, process the complete image
                        handle_send_image(connection, payload["phone_number"], image_data)
                        return

    except Exception as e:
        print(str(e))
    finally:
        connection.close()


def accept_connections(ServerSocket):
        client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        worker = threading.Thread(target=client_handler, args=(client, address))
        worker.start()

if __name__ == '__main__':
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
            events = sel.select(timeout=1)
            for key, mask in events:
                accept_connections(key.fileobj)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()
        for key, _ in sel.get_map().items():
            key.fileobj.close()
        mongoAPI.disconnect()