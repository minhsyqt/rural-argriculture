from pymongo import MongoClient
import rpyc
import json

<<<<<<< Updated upstream
=======
# globals 
#? should these be in a config file, encrypted?
HOST = "localhost"
MONGODB_SERVER = 'mongodb://localhost:27017/'
PORT = 27017

# global instantiations 
client = ""
collection = ""
database = ""
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream

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
=======
class MongoAPI(rpyc.Service):
    def on_connect(self, conn, _database, _collection):
        global client, collection, database
        client = MongoClient(MONGODB_SERVER, PORT, directConnection=True)
        database = client[_database]
        collection = database[_collection]
    def on_disconnect(self, conn):
        global client
        client.close()

    def getUser(self, phoneNumber):
        global collection
        data = collection.find_one({"phone_number": phoneNumber})
>>>>>>> Stashed changes
        # data is a dict
        if (data is not None):
            return data
        else:
            return "User not found."
<<<<<<< Updated upstream
        
    # private method; expects a valid user object
    def _setUser(self, user):
        return self.collection.insert_one(user)
=======
    
        # private method; expects a valid user object
    def _setUser(self, user):
        global collection
        return collection.insert_one(user)
>>>>>>> Stashed changes

    # create user based on provided information
    def createUser(self, user):
        valid = _validateUser(user)
        if valid == True:
            return self._setUser(user)
        else:
            return "User could not be created: " + valid

<<<<<<< Updated upstream


    # fetch all users -> coordinates + phone numbers
    def getAllUsers(self):
        data = list(self.collection.find(projection=
=======
    # fetch all users -> coordinates + phone numbers
    def getAllUsers(self):
        global collection
        data = list(collection.find(projection=
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        return
=======
>>>>>>> Stashed changes

if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MongoAPI, port=18862, protocol_config={'allow_public_attrs': True}) # attributes that start with '_' will be private
<<<<<<< Updated upstream
    t.start()
    
=======
    t.start()
>>>>>>> Stashed changes
