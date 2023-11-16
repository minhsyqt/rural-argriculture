from pymongo import MongoClient
import rpyc
import json


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


# globals 
#? should these be in a config file, encrypted?
HOST = "localhost"
MONGODB_SERVER = 'mongodb://localhost:27017/'
PORT = 27017

# change to __init__ ?
# properties hosted in class obj, not globals?

class MongoAPI(rpyc.Service):
    #class instantiations
    connection = ""
    client = ""
    database = ""

    # connect, requires database and collection name
    def on_connect(self, conn):
        print("Socket bound.")
        
        pass

    def open(self, _database, _collection):
        self.client = MongoClient(MONGODB_SERVER, PORT, directConnection=True)
        self.database = self.client[_database]
        self.collection = self.database[_collection]

    # disconnect -> garbage collection
    def on_disconnect(self, conn):
        print("Socket in listening state.")
        pass

    def close(self):
        self.client.close()
        print("MongoAPI connection closed.")

    def getUser(self, phoneNumber):
        data = self.collection.find_one({"phone_number": phoneNumber})
        # data is a dict
        if (data is not None):
            return data
        else:
            return "User not found."
        
    # private method; expects a valid user object
    def _setUser(self, user):
        return self.collection.insert_one(user)

    # create user based on provided information
    def createUser(self, user):
        valid = _validateUser(user)
        if valid == True:
            return self._setUser(user)
        else:
            return "User could not be created: " + valid



    # fetch all users -> coordinates + phone numbers
    def getAllUsers(self):
        data = list(self.collection.find(projection=
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

if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MongoAPI, port=18862, protocol_config={'allow_public_attrs': True}) # attributes that start with '_' will be private
    t.start()
    