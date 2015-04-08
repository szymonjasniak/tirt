import FileReader

from twisted.internet import reactor
from twisted.python import log

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS


class EchoClientProtocol(WebSocketClientProtocol):
    lineNumber = 0

    def sendHello(self):
        aklasa = FileReader.FileReader('flashcards.dictionary.com-error.log.4')
        self.sendMessage(aklasa.readLine(self.lineNumber).encode('utf8'))
        self.lineNumber += 1
        
    def sendPassword(self):
        self.sendMessage("pass".encode('utf8'))

    def onOpen(self):
        #self.sendHello()
        self.sendPassword()

    def onClose(self, wasClean, code, reason):
        print(reason)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))
        reactor.callLater(1, self.sendHello)


class EchoClientFactory(WebSocketClientFactory):

    protocol = EchoClientProtocol

    def clientConnectionLost(self, connector, reason):
        print(reason)
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        reactor.stop()


if __name__ == '__main__':

    adres='ws://127.0.0.1:9000/szymon'
    if len(adres) < 2:
        print("Need the WebSocket server address, i.e. ws://localhost:9000/echo1")

    factory = EchoClientFactory(adres)
    connectWS(factory)

    reactor.run()