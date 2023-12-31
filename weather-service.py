import json
import requests
import rpyc
import time
import math

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
        start = time.time()
        url = URL + "&q=" + str(round(user['location']['latitude'],7)) + "," + str(round(user['location']['longitude'],7)) + "&aqi=yes"
        weather_response = requests.get(url, headers=Headers).text
        weather_json = json.loads(weather_response)
        # trim down the fat. 
        # LOCATION: region, country, localtime,
        # CONDITONS: condition, temperature, wind speed, air quality
        weather = {
            "region": weather_json['location']['region'],
            "country": weather_json['location']['country'],
            "localtime": weather_json['location']['localtime'],
            "weather": weather_json['current']['condition']['text'],
            "temperature": weather_json['current']['temp_c'], #celcius
            "windspeed": weather_json['current']['wind_kph'], #kph
            "airquality": weather_json['current']['air_quality']['us-epa-index'] 
            
        }
        
        end = time.time()
        #?print(end-start)
        print(str(user['location']['latitude']) + "," + str(user['location']['longitude'])+ " was accessed in " + str(round(end-start,3)) +"s.")
        return weather

    # call all users' locations in database; create alerts for conditions containing:
    # Blizzard, Freezing rain, Hail, Heavy Rain, Strong Wind, Thunderstorm
    # also look for air quality - anything 4-6 is unhealthy; 7+ is severe
    cond_list = ["Freezing", "Hail", "Heavy", "Strong", "Thunderstorm"]
    def generate_alerts(self):
        # fetch list of all users
        mongoAPI_service = (rpyc.connect("localhost", 18862)).root
        mongoAPI_service.open("World", "Farmers")
        userList = mongoAPI_service.getAllUsers()
        mongoAPI_service = None
        
        #determine if any alerts
        counter = 0
        for user in userList:
            weather = self.fetch_weather(user)
            if any(condition in weather['weather'] for condition in self.cond_list):
                self.store_alert("WEATHER", weather['weather'], user['phone_number'])
                counter+=1
            if int(weather["airquality"]) > 6:
                self.store_alert("AIR QUALITY", weather["airquality"], user['phone_number'])
                counter+=1
            #?print(weather["airquality"])
            #?print(weather['weather'])
        return counter
    
    # fetches alerts stored in mongo collection; pushes them to users
    def fetch_alerts():
        #TODO
        pass

    # takes in an alert and stores it.
    def store_alert(self, type, weather, phonenumber):
        start = time.time()
        mongoAPI_service = (rpyc.connect("localhost", 18862)).root
        mongoAPI_service.open("World", "Alerts")
        alert = {
            "type": type,
            "value": weather,
            "phonenumber": phonenumber
        }
        mongoAPI_service.storeAlert(alert)
        end = time.time()
        print("Alert: "+ alert + ", stored in " + str(round(end-start, 3)) + "s.")
            

if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(Weather, port=18861, protocol_config={'allow_public_attrs': True}) # attributes that start with '_' will be private
    t.start()