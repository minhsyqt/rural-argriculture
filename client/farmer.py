from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import socket
import argparse
import json
import jwt
import random
import time

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
            start_time = time.time()
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
                    #print("Connected to server")
                except socket.error as e:
                    print(str(e))
                try:
                    # Send data
                    sock.send(json.dumps(signup_data).encode("utf-8"))
                    # Receive data from the server
                    received = json.loads(sock.recv(1024).decode("utf-8"))
                    #print("Received: {}".format(received))
                    sock.close()
                except socket.error as e:
                    print(str(e))
                    print("Server is down")
                finally:
                    sock.close()
            end_time = time.time()
            print("%f"%(end_time - start_time))

    def send_image(self, port_num):
            # Setup connection to host
            start_time = time.time()
            HOST = "localhost"
            PORT = 1024 + port_num

            # Placeholder, change to real farmer data if needed
            image_dim = 224
            sample_image = [random.randint(1, 256) for _ in range(image_dim * image_dim * 3)]

            # Create a socket (SOCK_STREAM means a TCP socket)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to the server
                try:
                    sock.connect((HOST, PORT))
                except socket.error as e:
                    print(str(e))
                    return

                try:
                    # Send data in chunks (64 pixels at a time)
                    chunk_size = 1024
                    total_pixels = len(sample_image)
                    num_chunks = (total_pixels + chunk_size - 1) // chunk_size  # Ceiling division

                    for i in range(num_chunks):
                        start_index = i * chunk_size
                        end_index = min((i + 1) * chunk_size, total_pixels)
                        chunk_data = sample_image[start_index:end_index]

                        image_data = {
                            "request_type": "send_image",
                            "phone_number": self.phone_number,
                            "chunk_data": chunk_data,
                            "chunk_index": i,
                            "total_chunks": num_chunks
                        }
                        # make sure the payload is less than 4096 bytes
                        # print((json.dumps(image_data).encode("utf-8")))

                        sock.sendall(json.dumps(image_data).encode("utf-8")+b"\n")

                    # Receive data from the server
                    response = json.loads(sock.recv(1024).decode("utf-8"))
                    # print("Received: {}".format(response))
                except socket.error as e:
                    print(str(e))
                finally:
                    sock.close()

            end_time = time.time()
            print("%f" % (end_time - start_time))