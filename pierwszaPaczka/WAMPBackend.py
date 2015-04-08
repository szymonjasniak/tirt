'''
Created on 7 kwi 2015

@author: Adrian
'''
import random
from datetime import datetime

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
class Component(ApplicationSession):

    """
    An application component that publishes events with no payload
    and with complex payload every second.
    """

    @inlineCallbacks
    def onJoin(self, details):
       
        print("session attached")
        
        
        
        counter = 0
        while True:
            timeStamp=datetime.now().time().strftime('%H:%M:%S')
            ##print(".")
            self.publish('com.myapp.heartbeat')

            obj = {'counter': counter, 'foo': [1, 2, 3]}
            self.publish('com.myapp.topic2', 1, timeStamp, c="Hello", d=obj)
            print("published : {0} on {1}".format(1,timeStamp))

            counter += 1
            yield sleep(random.randint(0, 10)/10)
         

if __name__ == '__main__':
    import sys
    from twisted.python import log
    from autobahn.twisted.wamp import ApplicationRunner
    log.startLogging(sys.stdout)
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    runner.run(Component)
