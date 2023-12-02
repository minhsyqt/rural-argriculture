import rpyc
import json
import time

def timerDaily():
    # fetches all alarms that available from sources
    # looks for 5am UTC every day to clear out mongoDB queue 
    pass


# every day, send out list of alarms sitting in the mongodb collection via a text
class Alarm(rpyc.Service):
    def on_connect(self, conn):
        print("Socket bound.")
        return super().on_connect(conn)
    
    def on_disconnect(self, conn):
        print("Socket listening.")
        return super().on_disconnect(conn)
    
    def DailyAlarms():
        # function is called every day by timerdaily
        mongo_service = (rpyc.connect("localhost", 18862)).root
        userlist = mongo_service.getAllUsers()
        # need function to grab alarms in mongoDB queue
    
    # searches for alarms from sources
    def FetchAlarms():
        pass
    
if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(Alarm, port=18864, protocol_config={'allow_public_attrs': True}) # attributes that start with '_' will be private
    t.start()
    timerDaily()