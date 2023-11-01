import mongoAPI
import requests

# https://api.weather.gov/points/{latitude},{longitude}
BaseURL = "https://api.weather.gov/points/"
Headers = {"Content-Type":"application/json"}

# weather calls
def _fetchWeather(user):
    url = BaseURL + str(user['location']['latitude']) + "," + str(user['location']['longitude'])
    weather = requests.get(url, headers=Headers) 
    #TODO : add correct headers; break apart weather
    return

# alerts calls
def _fetchAlert(user):
    # TODO : Implement
    return

def main():
    # fetch all users
    mongoAPI.connect("World", "Farmers")
    users = mongoAPI.getAllUsers()
    mongoAPI.disconnect()

    for user in list(users):
        # weather alerts
        _fetchWeather(user)

        # alerts

if __name__ == '__main__':
    main()