from pymongo import MongoClient
import json


# validates user based on provided dictionary
def validateUser(dict):
    if dict['phone_number'] == None:
        return "Invalid Phone Number."
    # elif (dict['firstname'] == None) and (dict['lastname'] == None):
    #     return "No name given"
    elif (dict['location']['longitude'] == None) or (dict['location']['latitude'] == None):
        return "invalid coordinates."
    elif (dict['location']['country'] == None): #At least the country name should be available
        return "invalid city/country names."
    else:
        return True

def validateImageEntry(entry):
    if entry['phone_number'] == None:
        return "Invalid Phone Number."
    elif (len((entry['image_data'])) != 224*224*3):
        return "Wrong Image Dimensions"
    else:
        return True

# globals 
#? should these be in a config file, encrypted?
HOST = "localhost"
MONGODB_SERVER = 'mongodb://localhost:27017/'
PORT = 27017

# global instantiations 
client = ""
collection = ""
database = ""

# connect, requires database and collection name
def connect(_database, _collection):
    global client, collection, database
    client = MongoClient(MONGODB_SERVER, PORT, directConnection=True)
    database = client[_database]
    collection = database[_collection]

# disconnect -> garbage collection
def disconnect():
    global client
    client.close()

def getUser(phoneNumber):
    global collection
    data = collection.find_one({"phone_number": phoneNumber})
    # data is a dict
    if (data is not None):
        return data
    else:
        return "User not found."

# create user based on provided information
def createUser(user):
    valid = validateUser(user)
    if valid == True:
        return _setUser(user)
    else:
        return "User could not be created: " + valid

def createImageEntry(entry):
    valid = validateImageEntry(entry)
    if valid == True:
        return _setUser(entry)
    else:
        return "Image cannot be inserted " + valid

# private method; expects a valid user object
def _setUser(user):
    global collection
    return collection.insert_one(user)

# fetch all users -> coordinates + phone numbers
def getAllUsers():
    global collection
    data = list(collection.find(projection=
    {
        "_id": 0,
        "phone_number": 1,
        "location.latitude": 1,
        "location.longitude": 1,
        "location.city": 1,
        "location.county": 1,
        "location.state": 1,
        "location.country": 1
    }))
    if (data is not None):
        return data
    else:
        return "User not found."
    return