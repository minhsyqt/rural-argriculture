from world import World
if __name__ == '__main__':

	num_farmers = 10000
	num_signup_per_day = 2
	DAYS = 1

	seed = 0

	lat_start = 0
	lat_stop = 100
	long_start = 0
	long_stop = 100

	world = World(num_farmers, seed, lat_start, lat_stop, long_start, long_stop)

	for day in range(DAYS):
		print("===============Day %d=============="%day)
		world.next_day(num_signup_per_day)
