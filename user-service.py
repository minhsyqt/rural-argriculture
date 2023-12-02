import rpyc
import json

class User(rpyc.Service):
    def on_connect(self, conn):
        return super().on_connect(conn)
    def on_disconnect(self, conn):
        return super().on_disconnect(conn)
    
    # initiate client connection
    def connectMongo(self):
        self.MongoService = (rpyc.connect("localhost", 18862)).root
    
    # garbage cleanup
    def disconnectMongo(self):
        self.MongoService.close()

    def NewUser(self, User):
        self.connectMongo()
        # push json string, or dict?
        self.MongoService.createUser(User)
        pass

    def EditUser(self):
        self.connectMongo()
        # push json string, or dict?
        # TODO
        pass

    def DeleteUser():
        # TODO
        pass
    

if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(User, port=18863, protocol_config={'allow_public_attrs': True}) # attributes that start with '_' will be private
    t.start()