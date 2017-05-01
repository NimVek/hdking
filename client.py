#!/usr/bin/env python

import cmd
import SocketServer
import threading
import socket
import hdking


class TCPControlHandler(SocketServer.StreamRequestHandler):
    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.connection = hdking.HDKingStatelessConnection(self.rfile, self.wfile)

    def handle(self):
	self.connection.send(hdking.HDKingPacketLoginRequest())
        for packet in self.connection:
	    if packet.opcode == 0x112:
		self.connection.send(hdking.HDKingPacketKeepAliveResponse())
            print("%s" % packet)


class TCPControl(object):
    def connect(self, server):
        self.server = server
        self.thread = threading.Thread(target=self.run,
                                       name=self.__class__.__name__)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server, 6666))
        TCPControlHandler(self.socket, (self.server, 6666), self)


class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'HDKing: '
#	super(Console, self).__init__()

    def do_EOF(self, line):
        return True

    def emptyline(self):
        pass

    def do_connect(self, line):
        self.client = TCPControl()
        self.client.connect('192.168.100.1')

    def do_threads(self, line):
        for thread in threading.enumerate():
            print thread

if __name__ == '__main__':
    Console().cmdloop()
