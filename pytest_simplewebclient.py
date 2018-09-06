#!/usr/bin/python3
import asyncio, sys, time, os

def checkFile():
    files = os.listdir();
    numAsChar = ord('0');
    for file in files:
        if 'web_response' in file:
            if ord(file[-5]) > numAsChar:
                numAsChar=ord(file[-5]);
    return chr(numAsChar+1);
def makeHttp(message):
    snd=b'GET ' + message.encode() + b' HTTP/1.1'
    return snd

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport=None;

    def connection_made(self, transport):
        self.transport=transport;
        transport.write(makeHttp(self.message));
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        recv = data.decode().split('\n');
        code = recv[0].split()[1];
        time = recv[1];
        if code == '200':
            content = recv[2];
        
        numFile = checkFile();
        with (open("web_response_"+numFile+".txt", "w+")) as outFile:
            outFile.write(time);
            outFile.write(self.message + '\n')
            outFile.write(code + '\n')
            if code == '200':
                outFile.write(content)
        outFile.close();
        print('finished writing to file');
        loop.stop();
                
    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = 'hello'
port = sys.argv[1]
message=sys.argv[2]

coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              '127.0.0.1', port)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()