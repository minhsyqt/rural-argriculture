import time
import rpyc

weather_service = (rpyc.connect("localhost", 18861)).root
mongoAPI_service = (rpyc.connect("localhost", 18862)).root

mongoAPI_service.open("World", "Farmers")
user = mongoAPI_service.getUser("168-696-9935")

value = weather_service.fetch_weather(user)

print(value)