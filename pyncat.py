#!/usr/bin/env python
#coding=utf-8

import socket
import argparse
import multiprocessing
import select

class server:
    def __init__(self,bport,pip,pport,multi):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('0.0.0.0',bport))
        self.serversocket.listen(multi)
        self.dport=(pip,dport)
        self.multi=multi
        self.plist=[]
        
    def newconnect(self,clientsocket):
        proxysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'newconnect',self.dport
        proxysocket.connect(self.dport)
        while True:
            if not self.trans(clientsocket,proxysocket):break
        proxysocket.close()
        clientsocket.close()
        
    def trans(self,csocket,proxysocket):
        rdata,wdata,edata = select.select([csocket,proxysocket],[],[],5) #非阻塞方式实现双工
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
        for mu in range(self.multi):#限制访问次数
            clientsocket , clientaddress = self.serversocket.accept()
            p = multiprocessing.Process(target=self.newconnect, args=(clientsocket, ))
            p.start()
            self.plist.append(p)
        return True
        
    def close(self):
        for p in self.plist:
            p.join()
        self.serversocket.close()

def getargv():
    parser = argparse.ArgumentParser(description="""sudo python pyncat.py -l 80 -i www.google.com -p 80 -k 100""")
    parser.add_argument("-l", dest='bport',help="bind port",type=int,default=8086)
    parser.add_argument('-i', dest='pip',help='proxy ip',type=str,default='127.0.0.1')
    parser.add_argument('-p', dest='pport',help='proxy ip',type=int,default=8088)
    parser.add_argument('-k', dest='multi',help='multi connect',type=int,default=1)
    args = parser.parse_args()
    return args
    
if __name__ == "__main__":
    args=getargv()
    proxy=server(args.bport,args.pip,args.pport,args.multi)
    try:
        proxy.run()
    except KeyboardInterrupt:
        proxy.close()
