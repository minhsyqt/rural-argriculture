import mongoAPI
import weather
import time
import rpyc

weather_service = (rpyc.connect("localhost", 18861)).root

mongoAPI.connect("World", "Farmers")
user = mongoAPI.getUser("168-696-9935")
mongoAPI.disconnect()

value = weather_service.fetch_weather(user)

print(value)