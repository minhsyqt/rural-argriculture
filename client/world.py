# Use world to spawn farmers, asign geolocation, and call farmers actions

import Farmer

class World:
    def __init__(self, num_farmers, seed, lat_start, lat_stop, long_start, long_stop):
    	self.seed = seed
    	self.farmers = []

    	for i in range(num_farmers):
    		# pick a random geolocation
    		geolocation = {"lat" : random.uniform(lat_start, lat_stop), "long" : random.uniform(long_start, long_stop)}
    		self.farmers.append(Farmer(i, geolocation))

   	def next_day():
   		pass