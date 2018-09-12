#!/usr/bin/python3

import asyncio, sys, time, os,random

balls={};
resps=['Your guess is as good as mine.',
       'You need a vacation.',
       "It's Trump's fault!",
       "I don't know. What do you think?",
       "Nobody ever said it would be easy, they only said it would be worth it.",
       "You really expect me to answer that?",
       "You're going to get what you deserve.",
       "That depends on how much you're willing to pay."
       ]

def checkFile():
    files = os.listdir();
    numAsChar = ord('0');
    for file in files:
        if '8ball_message' in file:
            if ord(file[-5]) > numAsChar:
                numAsChar=ord(file[-5]);
    return chr(numAsChar+1);

def make_response(msg):
    balls[msg] = random.choice(resps);
    return balls[msg];


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
    
        resp = None;
        if(message == '__EXIT__'):
            print('Stopping server')
            self.transport.close()
            loop.stop();
        else:
            if message in balls.keys():
                resp = balls[message];
            else:
                resp = make_response(message);
            self.transport.write(resp.encode());
        numFile = checkFile();
        with (open("8ball_message_"+numFile+".txt", "w+")) as outFile:
            outFile.write(str(time.time())+'\n');
            outFile.write(message + '\n');
            outFile.write(resp)
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
