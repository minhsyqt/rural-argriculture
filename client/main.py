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

	for day in range(DAYS):
		print("===============Day %d=============="%day)
		world.next_day(num_signup_per_day)
