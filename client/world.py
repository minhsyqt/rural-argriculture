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
        for i in range(num_farmers):
            # pick a random geolocation
            geolocation = {"lat" : random.uniform(lat_start, lat_stop), "long" : random.uniform(long_start, long_stop)}
            phone_number = ''.join(random.choices('0123456789', k=9))
            self.farmers.append(Farmer(phone_number, geolocation))

    def register_farmers(self, num_signup_per_day):
        sample_list = range(0, self.num_farmers)
        signup_num = 0
        for i in random.sample(sample_list, num_signup_per_day):
            self.farmers[i].signup(signup_num)
            signup_num += 1

    def send_plant_images(self, num_images):
        sample_list = range(0, self.num_farmers)
        signup_num = 0
        for i in random.sample(sample_list, num_images):
            self.farmers[i].send_image(signup_num)
            signup_num += 1