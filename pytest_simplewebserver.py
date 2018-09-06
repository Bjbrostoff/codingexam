#!/usr/bin/python3

import asyncio, sys, time, os

def findfile(filepath):
    pathToServer = sys.argv[2];
    if filepath in os.listdir(pathToServer):
        return '200',os.path.abspath(filepath)
    else:
        return '404',None;
    
def checkFile():
    files = os.listdir();
    numAsChar = ord('0');
    for file in files:
        if 'web_message' in file:
            if ord(file[-5]) > numAsChar:
                numAsChar=ord(file[-5]);
    return chr(numAsChar+1);

def make_response(filepath):
    code,fullpath = findfile(filepath)
    head  = b'HTTP/1.1 ';
    head += code.encode() + b' OK\r\n';
    head += str(time.time()).encode() + b'\r\n';
    if fullpath:
        head+= fullpath.encode() + b'\r\n';
#     head += b'Content-Type: text/html\r\n'
#     head += b'\r\n'
    return head


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        
        mList=message.split();
        filepath=mList[1];
        
        if(filepath == 'EXIT'):
            print('Stopping server')
            self.transport.close()
            loop.stop();
        else:
            resp=make_response(filepath);
            self.transport.write(resp);
        numFile = checkFile();
        with (open("web_message_"+numFile+".txt", "w+")) as outFile:
            outFile.write(resp.decode());
        print('finished writing to file');
        outFile.close();


loop = asyncio.get_event_loop()
# Each py connection will create a new protocol instance

port = sys.argv[1];


coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', port)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
