from pymongo import MongoClient
import json

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
    client.close()

def getUser(phoneNumber):
    data = collection.find_one({"phone_number": phoneNumber})
    if (data is not None):
        return data 

# create user based on provided information
def createUser():
    # collection.insert_one()
    return

# check for parameter; change that one 
def setUser():
    return