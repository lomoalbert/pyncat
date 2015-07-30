import socket
import select

class server:
    def __init__(self,bport,pip,pport):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('0.0.0.0',bport))
        self.serversocket.listen(1)
        self.dport=(pip,pport)
        
    def newconnect(self,clientsocket):
        proxysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'newconnect',self.dport
        proxysocket.connect(self.dport)
        while True:
            if not self.trans(clientsocket,proxysocket):break
        proxysocket.close()
        clientsocket.close()
        
    def trans(self,csocket,proxysocket):
        rdata,wdata,edata = select.select([csocket,proxysocket],[],[],5) 
        if csocket in rdata:
            data = csocket.recv(1024)
            if not data :return False
            proxysocket.send(data)
        elif proxysocket in rdata:
            data = proxysocket.recv(1024)
            if not data :return False
            csocket.send(data)
        return True
            
    def run(self):
        while True:
            clientsocket , clientaddress = self.serversocket.accept()
            self.newconnect(clientsocket)
        return True
        
    
if __name__ == "__main__":
    args=getargv()
    proxy=server(80,'mirrors.sohu.com',80)
    try:
        proxy.run()
    except KeyboardInterrupt as err:
        print err
