import time
import rpyc

weather_service = (rpyc.connect("localhost", 18861)).root
mongoAPI_service = (rpyc.connect("localhost", 18862)).root

mongoAPI_service.open("World", "Farmers")
user = mongoAPI_service.getUser("429662249")


weather_service.generate_alerts()

#userList = mongoAPI_service.getAllUsers()
#for user in userList:
    #weather_service.fetch_weather(user)

value = weather_service.fetch_weather(user)

print(value)