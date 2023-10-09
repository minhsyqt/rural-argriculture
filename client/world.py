# Use world to spawn farmers, asign geolocation, and call farmers actions
from farmer import Farmer
import random
import socket
import time
from _thread import *
import argparse
import json

class World:
    def __init__(self, num_farmers, seed, lat_start, lat_stop, long_start, long_stop):
        self.seed = seed
        self.farmers = []
        self.num_farmers = num_farmers
        self.sock = None
        # Setup conneciton to host
        HOST = "localhost"
        PORT = 9999

        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server 
            try:
                sock.connect((HOST, PORT))
                print("Connected to server")
            except socket.error as e:
                print(str(e))

        self.sock = sock
        for i in range(num_farmers):
            # pick a random geolocation
            geolocation = {"lat" : random.uniform(lat_start, lat_stop), "long" : random.uniform(long_start, long_stop)}
            self.farmers.append(Farmer(i, geolocation, self.sock))

    def next_day(self, num_signup):
        sample_list = range(0, self.num_farmers)
        for i in random.sample(sample_list, num_signup):
            self.farmers[i].signup()