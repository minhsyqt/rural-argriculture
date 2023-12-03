from pymongo import MongoClient
import rpyc

# globals 
#? should these be in a config file, encrypted?
HOST = "localhost"
MONGODB_SERVER = 'mongodb://localhost:27017/'
PORT = 27017

# global instantiations 
client = ""
collection = ""
database = ""

# validates user based on provided dictionary
def _validateUser(dict):
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

class MongoAPI(rpyc.Service):
    def on_connect(self, conn):
        print("Socket Bound.")
        pass
    def on_disconnect(self, conn):
        global client
        client.close()
        print("Socket closed. MongoDB client closed.")
        pass
    
    def open(self, _database, _collection):
        global client, collection, database
        client = MongoClient(MONGODB_SERVER, PORT, directConnection=True)
        database = client[_database]
        collection = database[_collection]

    def getUser(self, phoneNumber):
        global collection
        data = collection.find_one({"phone_number": phoneNumber})
        # data is a dict
        if (data is not None):
            print(phoneNumber + " accessed.")
            return data
        else:
            print(phoneNumber + " failed to find.")
            return ("User not found.")
    
    # private method; expects a valid user object
    def _setUser(self, user):
        global collection
        return collection.insert_one(user)

    # create user based on provided information
    def createUser(self, user):
        valid = _validateUser(user)
        if valid == True:
            return self._setUser(user)
        else:
            return "User could not be created: " + valid

    # fetch all users -> coordinates + phone numbers
    def getAllUsers(self):
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
    
    def createImageEntry(self, entry):
        valid = validateImageEntry(entry)
        if valid == True:
            return self._setUser(entry)
        else:
            return "Image cannot be inserted " + valid
    
    def getNewImages(self):
        global collection

        # Find documents where the "done" field is "false" (as a string)
        documents = list(collection.find({"done": "false"}))

        # Update the "done" field to "true" for the retrieved documents
        result = collection.update_many(
            {"done": "false"},
            {"$set": {"done": "true"}}
        )

        return list(documents)
    
    def storeAlert(self, alert):
        global collection
        print(alert)
        return collection.insert_one(alert)


if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MongoAPI, port=18862, protocol_config={'allow_public_attrs': True}) # attributes that start with '_' will be private
    t.start()
    
