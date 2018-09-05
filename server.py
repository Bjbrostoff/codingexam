#!/usr/bin/python3

import asyncio, sys, time

def encrypt(message):
    toEncrypt = message.split(',')[1];
    output = [];
    for c in list(toEncrypt):
        output.append(chr(ord(c)+1))
    return ''.join(output);
def decrypt(message):
    toDecrypt = message.split(',')[1];
    output = [];
    for c in list(toDecrypt):
        output.append(chr(ord(c)-1))
    return ''.join(output);
    with(open("security_message_1.txt", "w+")) as outFile:
        outFile.write(time.time() + '\n')
        outFile.write(''.join(output) + '\n')
        outFile.write(toDecrypt);

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()
        if(message == 'EXIT'):
            print('Stopping server')
            loop.stop();
        elif('encrypt' in message):
            self.transport.write(('cypher,'+encrypt(message)).encode());
        elif('decrypt' in message):
            self.transport.write(('plain,'+decrypt(message)).encode());

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance

port = sys.argv[1];


coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', port)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
