import requests
import time
import random

openCage_api_key = 'b0771141718d418891a88be91a30574a'
rate_limit = 5 # seconds
max_attempt = 10

def get_city_country(latitude, longitude):
	attempt = 0
	city = "N/A"
	county = "N/A"
	state = "N/A"
	country = "N/A"

	while (attempt < max_attempt):
		attempt += 1
		url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={openCage_api_key}'
		response = requests.get(url)

		if (response.status_code == 200):
			print("Success for %f, %f, attempt %d"%(latitude,longitude, attempt))
			data = response.json()
			if 'results' in data and data['results']:
			    result = data['results'][0]
			    city = result.get('components', {}).get('city', 'N/A')
			    county = result.get('components', {}).get('county', 'N/A')
			    state = result.get('components', {}).get('state', 'N/A')
			    country = result.get('components', {}).get('country', 'N/A')
			break
		else:
			print("Failed for %f, %f, attempt %d"%(latitude,longitude, attempt))
			time.sleep(random.randint(0,10))
	return city, county, state, country
