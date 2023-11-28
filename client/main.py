from world import World
if __name__ == '__main__':

	num_farmers = 10000
	num_signup_per_day = 2
	DAYS = 2

	seed = 0

	lat_start = 18
	lat_stop = 30
	long_start = 19
	long_stop = 30

	world = World(num_farmers, seed, lat_start, lat_stop, long_start, long_stop)

	# Different experiment to be ran
	
	#world.register_farmers(500)
	world.send_plant_images(10)
