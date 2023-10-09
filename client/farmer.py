from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import socket
import argparse
import json

class Farmer:
    def __init__(self, farmerID, geolocation, sock):
        self.farmerID = farmerID
        self.geolocation = geolocation
        self.sock = sock
        self.already_signup = False

        # Signup related
        self.private_key = None
        self.public_key = None
        self.cloudlab_token = None
        self.already_signup = False
        self.public_key_json = None

    #================= Actions that farmers can do =================

    # The first action should always be sign up, onetime event
    # 1) generate RSA private, public key
    # 2) send public key to cloudlab through API
    # 3) receive token from cloudlab
    def signup(self):
        if not self.already_signup:
            # Generate an RSA key pair
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            # Serialize the private and public keys to PEM format
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            public_pem = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Store the keys
            self.private_key = private_pem
            self.public_key = public_pem
            self.already_signup = True

            # Convert the PEM bytes to a string
            self.public_key_json = public_pem.decode('utf-8')

            try:
                # Send data
                self.sock.send(json.dumps(self.public_key_json).encode("utf-8"))
                # Receive data from the server
                received = json.loads(self.sock.recv(2048).decode("utf-8"))
                print("Received: {}".format(received))
            except socket.error as e:
                print(str(e))
                print("Server is down")

    # Login: recuring first step everytime farmer connect to server
    # 1) pass token to cloudlab for verification
    # 2) send request for updates like weather, alarm
    def login(self):
        pass