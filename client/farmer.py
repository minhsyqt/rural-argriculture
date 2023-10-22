from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import socket
import argparse
import json
import jwt
import random

class Farmer:
    def __init__(self, phone_number, farm_location):
        self.farmerID = phone_number
        self.farm_location = farm_location
        self.already_signup = False

        # Signup related
        self.phone_number = phone_number # keep it simple ... 

    #================= Actions that farmers can do =================

    # The first action should always be sign up, onetime event
    def signup(self, signup_num):
        if not self.already_signup:
            # Setup conneciton to host
            HOST = "localhost"
            PORT = 1024 + signup_num

            signup_data = { "request_type": "signup",
                            "phone_number": self.phone_number,
                            "farm_location_lat": self.farm_location["lat"],
                            "farm_location_long": self.farm_location["long"]
                            }

            # Create a socket (SOCK_STREAM means a TCP socket)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server 
                try:
                    sock.connect((HOST, PORT))
                    print("Connected to server")
                except socket.error as e:
                    print(str(e))

                try:
                    # Send data
                    sock.send(json.dumps(signup_data).encode("utf-8"))
                    # Receive data from the server
                    received = json.loads(sock.recv(1024).decode("utf-8"))
                    print("Received: {}".format(received))
                    sock.close()
                except socket.error as e:
                    print(str(e))
                    print("Server is down")
                finally:
                    sock.close()

    # Login: recuring first step everytime farmer connect to server
    # 1) pass token to cloudlab for verification
    # 2) send request for updates like weather, alarm
    def login(self):
        pass