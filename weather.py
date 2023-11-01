import mongoAPI
import requests

# https://api.weather.gov/points/{latitude},{longitude}
BaseURL = "http://api.weatherapi.com/v1/current.json"
Headers = {
    "Content-Type":"application/json",
    "User-Agent": "Rural-Agriculture"
    }
API_KEY = "a661df6f200547508bb181510230111"
URL = BaseURL + "?key=" + API_KEY

# weather calls
def _fetchWeather(user):
    url = URL + "&q=" + str(user['location']['latitude']) + "," + str(user['location']['longitude']) + "&aqi=yes"
    weather = requests.get(url, headers=Headers).text
    #TODO : break apart weather
    return weather

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