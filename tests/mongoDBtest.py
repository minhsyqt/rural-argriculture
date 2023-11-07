# test file for debugging purposes only
import mongoAPI
import weather

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

#val = mongoAPI.createUser(newuser)
#newdata = mongoAPI.getAllUsers()
mongoAPI.disconnect()


#weather
alert = weather.main()

print(val)