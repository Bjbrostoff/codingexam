#!/usr/bin/python3
import asyncio, sys, time

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport=None;
        self.c = None;
        self.p = None;

    def connection_made(self, transport):
        self.transport=transport;
        messagept1 = ('encrypt,'+self.message).encode();
        transport.write(messagept1);
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        recv = data.decode();
        if('cypher' in recv):
            self.c = recv.split(',')[1];
            self.transport.write('decrypt,'+self.c)
        elif('plain' in recv):
            self.p = recv.split(',')[1];
            with (open("security_response_1.txt", "w+")) as outFile:
                outFile.write(time.time() + '\n');
                outFile.write(self.p)
                outFile.write(self.c)
                
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