# test file for debugging purposes only
import mongoAPI
import weather
import time

mongoAPI.connect("World", "Farmers")

print('got here!')

print(mongoAPI.getUser("206-294-1499"))

newuser = {
    "phone_number": "847-460-8249",
    "firstname": "simon",
    "lastname": "spivey",
    "location": {
        "latitude": 40.440624,
        "longitude": 40.440624
    }
}

'''
    mongoAPI.connect("World", "Farmers")
    users = mongoAPI.getAllUsers()
    mongoAPI.disconnect()

    for user in list(users):
        # weather alerts
        _fetchWeather(user)
'''

#val = mongoAPI.createUser(newuser)
#newdata = mongoAPI.getAllUsers()
mongoAPI.disconnect()


#weather
alert = weather.main()

print(val)