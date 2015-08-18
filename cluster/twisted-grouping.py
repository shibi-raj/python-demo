from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import basic
from twisted.web import client
import xml.etree.ElementTree as ET


class Protocol(basic.LineReceiver):
    def lineReceived(self, user):
        d = self.factory.getUser(user)

        def onError(err):
            return 'Internal error in server'
        d.addErrback(onError)

        def writeResponse(message): pass
            #self.transport.write(message + '\r\n')
            #self.transport.loseConnection()
        d.addCallback(writeResponse)

        def parseResponse(message):
            #self.transport.write(message + '\r\n')
            tree = ET.ElementTree(message)
            root = tree.getroot()
            self.transport.write(root + '\r\n')
            """
            for doc in root.iter(tag='doc'):
                display = []
                for each in doc.iter():
                    title = ''
                    try:
                        if each.attrib['name'] == 'title':  title = each.text
                    except: pass
                if each.text and not each.attrib: 
                    display.append( '  ' + each.text.lower() )
            #print title
            display.insert(0,title)
            for i,d in enumerate(display):
                if i == 0: print bold(d)
                else: print d
            print
            #self.transport.loseConnection()
            """
        d.addCallback(parseResponse)


class Factory(protocol.ServerFactory):
    protocol = Protocol
    
    def __init__(self, prefix):
        self.prefix=prefix
    
    def getUser(self, user):
        return client.getPage(self.prefix+user)


reactor.listenTCP(1079, Factory(prefix='http://localhost:8983/solr/select?q=sales&fq={!child%20of=%22type:parent%22}'))
reactor.run()



