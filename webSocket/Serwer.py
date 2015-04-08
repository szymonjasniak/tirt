from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
import json
import io
from time import gmtime, strftime
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS

from autobahn.websocket.http import HttpException


class BaseService:

    def __init__(self, proto):
        self.proto = proto

    def onOpen(self):
        pass

    def onClose(self, wasClean, code, reason):
        pass

    def onMessage(self, payload, isBinary):
        pass


class EchoService(BaseService):
    
    def onMessage(self, payload, isBinary):
          
        if not isBinary:
            msgToSave={'dana' : strftime("%Y-%m-%d %H:%M:%S", gmtime())+" "+payload.decode('utf-8')}
            with io.open('savedData.json', 'w', encoding='utf-8') as f:
                f.write(unicode(json.dumps(msgToSave, ensure_ascii=False, indent=2)))
            msg = "Wiadomosc - {}".format(payload.decode('utf8'))
            print(msg)
            self.proto.sendMessage(msg.encode('utf8'))
       
class ServiceServerProtocol(WebSocketServerProtocol):

    SERVICEMAP = {'/szymon': EchoService,
                  '/adrian': EchoService}

    def __init__(self):
        self.service = None

    def onConnect(self, request):
        
        print(request)
        print('raz')
        print(request.peer)
        print(request.headers)
        print(request.host)
        print('dwa')
        print(request.path)
        print(request.params)
        print(request.version)
        print('trzy')
        print(request.origin)
        print(request.protocols)
        print(request.extensions)

        if request.path in self.SERVICEMAP:
            cls = self.SERVICEMAP[request.path]
            self.service = cls(self)
        else:
            err = "No service under %s" % request.path
            print(err)
            raise HttpException(404, err)

    def onOpen(self):
        if self.service:
            self.service.onOpen()
        print('onOpen')

    def onMessage(self, payload, isBinary):
        if self.service:
            self.service.onMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        if self.service:
            self.service.onClose(wasClean, code, reason)


if __name__ == '__main__':

    factory = WebSocketServerFactory("ws://localhost:9000")
    factory.protocol = ServiceServerProtocol
    listenWS(factory)

    reactor.run()