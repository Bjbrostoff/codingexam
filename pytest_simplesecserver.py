#!/usr/bin/python3

import asyncio, sys, time,os
def checkFile():
    files = os.listdir();
    numAsChar = ord('0');
    for file in files:
        if 'security_message' in file:
            if ord(file[-5]) > numAsChar:
                numAsChar=ord(file[-5]);
    return chr(numAsChar+1);

def encrypt(message):
    toEncrypt = message.split(',')[1];
    output = [];
    for c in list(toEncrypt):
        output.append(chr(ord(c)+1))
    print('encrypted message: ' + ''.join(output))
    return ''.join(output);

def decrypt(message):
    toDecrypt = message.split(',')[1];
    output = [];
    for c in list(toDecrypt):
        output.append(chr(ord(c)-1))
    numFile = checkFile();
    with (open("security_message_"+numFile+".txt", "w+")) as outFile:
        outFile.write(str(time.time()) + '\n')
        outFile.write(''.join(output) + '\n')
        outFile.write(toDecrypt);
        print('finished writing to file');
    outFile.close();

    return ''.join(output);

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        
        if(message == 'EXIT'):
            print('Stopping server')
            self.transport.close()
            loop.stop();
        elif('encrypt' in message):
            self.transport.write(('cypher,'+encrypt(message)).encode());
        elif('decrypt' in message):
            self.transport.write(('plain,'+decrypt(message)).encode());

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
