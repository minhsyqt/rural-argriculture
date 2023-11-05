#need to reimplement to use mongoAPI
import socket
import time
from _thread import *
import threading
import argparse
import json
import selectors
import pymongo
import googlemaps
from pymongo import MongoClient

# Important Global Configurations
HOST = "localhost"
MONGODB_SERVER = 'mongodb://localhost:27017/'
NUM_PORTS = 256

#gmapsclient = googlemaps.Client(key='Ask Minh for API key')
openCage_api_key = 'b0771141718d418891a88be91a30574a'

# Global Variables
mongoclient = MongoClient(MONGODB_SERVER)
DB = mongoclient['farmers_database']
farmers_collection = DB['farmers_info']

def handle_signup(connection, payload):
    # Send reply back to client
    connection.sendall(json.dumps("Signup sucessful!").encode("utf-8"))

    latitude  = payload["farm_location_lat"]
    longitude = payload["farm_location_long"]
    api_key = openCage_api_key
    url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={api_key}'

    # Send a GET request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    # Extract city and country information from the response
    if 'results' in data and data['results']:
        result = data['results'][0]
        city = result.get('components', {}).get('city', 'N/A')
        country = result.get('components', {}).get('country', 'N/A')
        print(f'City: {city}, Country: {country}')
    else:
        print('Location information not found.')

    # Insert new entry into MongoDB
    collection_entry = {
        "phone_number": payload["phone_number"],
    }
    farmers_collection.insert_one(collection_entry)

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
            print("{}:{} wrote: {}".format(address[0], address[1], payload))

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
        mongoclient.close()