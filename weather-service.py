import mongoAPI
import json
import requests
import rpyc

# https://api.weather.gov/points/{latitude},{longitude}
BaseURL = "http://api.weatherapi.com/v1/current.json"
Headers = {
    "Content-Type":"application/json",
    "User-Agent": "Rural-Agriculture"
    }
API_KEY = "a661df6f200547508bb181510230111"
URL = BaseURL + "?key=" + API_KEY


class Weather(rpyc.Service):
    def on_connect(self, conn):
        print("Socket bound.")
        pass
    def on_disconnect(self, conn):
        print("Socket in listening state.")
        pass

    # weather calls
    def fetch_weather(self, user):
        url = URL + "&q=" + str(user['location']['latitude']) + "," + str(user['location']['longitude']) + "&aqi=yes"
        weather_json = requests.get(url, headers=Headers).text
        print(weather_json)
        weather = json.loads(weather_json)
        return weather

    # alerts calls
    def fetch_alert(self, user):
        # TODO : Implement
        return "string"

if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(Weather, port=18861, protocol_config={'allow_public_attrs': True}) # attributes that start with '_' will be private
    t.start()