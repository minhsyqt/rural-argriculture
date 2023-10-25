# test file for debugging purposes only
import mongoAPI

mongoAPI.connect("World", "Farmers")

print('got here!')

print(mongoAPI.getUser("630-386-0119"))

newuser = {
    "phone_number": "847-460-8249",
    "firstname": "simon",
    "lastname": "spivey",
    "location": {
        "location": {
            "0": 40.440624,
            "1": 40.440624
        }
    }
}

val = mongoAPI.createUser(newuser)
mongoAPI.disconnect()
print(val)